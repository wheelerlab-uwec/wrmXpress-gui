# 🌟🔧 Modular Mastery in Research GUIs 🌐🌟

Hello, digital explorers of science! 🚀 Are you ready to supercharge your research GUI with modular technology? 🎛️ This guide is crafted to help you seamlessly integrate new modules or combine existing ones within the "Run" page of your GUI. Let’s not just do research—let’s revolutionize it with modular efficiency! 🌌

## Module Integration Manifest for GUI 🛠️📊

Here's how we'll proceed with enhancing your research GUI's functionality:

| Module Element                | Exploration Guide                                                   |
|-------------------------------|---------------------------------------------------------------------|
| **Module Fundamentals** 📘      | Dive into the core concepts of using modules in a research GUI.     |
| **Designing Your Module** 🎨    | Steps to create a research module tailored to GUI needs.            |
| **Implementation Phases** 🔧    | How to implement and set up your module on the "Run" page.          |
| **Validation Techniques** ✔️   | Methods to ensure your module is performing as intended.            |
| **Synergy of Modules** 🤝      | Strategies for integrating multiple modules effectively.            |
| **Overcoming Challenges** 🚧   | Solutions for common issues in module integration.                  |
| **Specifics for the Run Page** 🏃 | Detailed instructions for integrating and using modules on this page.|
| **Handling Preview Page Logic** 👀 | How to manage conditional logic and output on the "Preview" page.   |

## Deep Dive into the GUI Pages 🤿📑

### Run Page
- **Integration and Activation** 🛠️: Learn to insert and activate new modules specifically tailored for the "Run" page. This section will guide you through combining multiple modules to expand the functionality and streamline the research process.

### Preview Page
- **Conditional Logic and Workflow** 🔄:
  - Check if the first well or any selected well has been analyzed 🧐.
  - If analyzed, return the associated figure directly 🖼️.
  - If not, copy only the selected well that hasn’t been analyzed 📋.
  - Run `wrmXpress` or a similar process on the copied well, details of which will be explained in the subsequent sections.

## Let’s Begin Our Modular Journey! 🌍🚀

### Step 1: Module Selection and Modification 📊

- **Location**: Go to `app/components/module_selection.py`.
- **Task**: Find the `dbc.RadioItems` component with the ID `pipeline-selection`. Here, you can:
  - **Add a Module** ➕: Insert new module options as necessary.
  - **Remove a Module** ➖: Delete options as necessary. Remember, if you remove modules, you must also adjust the corresponding function in `app/utils/callback_functions.py`.
- **Updating Functions** 🔄:
  - Modify `formatting_module_for_yaml` function to include any new modules added so they are formatted correctly for YAML output.

### Step 2: YAML Configuration 📝

- **Location**: Navigate to the `prep_yaml` function in `app/utils/callback_functions.py`.
- **Task**: Ensure the newly added module has proper formatting in `yaml_dict` using the `eval_bool` function.
- **Testing** 🧪: Before proceeding, test to ensure the YAML file is correctly formatted and can be saved. If issues arise:
  - **Location**: Go to `app/pages/configure.py`.
  - **Modification**: Adjust the `run_analysis` function to account for the new module.

### Step 3: File Preparation and Module Execution 🗂️🚀

- **Process**:
  - Once the YAML file is correctly set up, copy the necessary files and run `wrmXpress` with the new module.
  - Follow the existing logic used in Docker/Python processes as outlined in the guide.

### Step 4: Integrating the Module into the Run Process 🔄

- **Location**: Go to `app.py` and find the `background_callback` function.
- **Task**: This function processes the execution when the "Run" button is clicked. Here, ensure that the newly added module is incorporated within the `callback` function found in `app/utils/background_callbacks.py`.
- **New Function** 🆕:
  - Create a new function specific to the module within `background_callbacks.py`.
  - **Note**: Each module might produce unique print statements from `wrmXpress`; ensure these are handled appropriately. If the outputs are consistent or a new tracking method is developed, significant changes to this process might be required.

### Future Considerations 💡

- **Improvements** 🌟: As the code and its architecture evolve, the process for adding or modifying modules may become more streamlined and efficient.
- **Tracking** 📊: Consider developing a method to track module progress more effectively, regardless of the specific module used. This will likely enhance the efficiency of the entire system.

## Let’s Continue Our Modular Integration Journey! 🛤️🔍

### Step 5: Implementing Specific Module Logic for ImageExpress Files 📸

- **Preparation**:
  - Begin by calling the `preamble_run_wrmXpress_imageexpress_selection` function. This function takes the argument `store` and returns a modified `store` while setting up the environment for running `wrmXpress`.
  - It will clear necessary directories, copy required files, and provide critical parameters like `wrmxpress_command_split`, `output_folder`, `output_file`, `wells`, `volume`, `platename`, and `plate_base`.

- **Running the Module** 🏃:
  - Open the `output_file` to log the output from the `wrmXpress` process:
    ```python
    with open(output_file, "w") as file:
        process = subprocess.Popen(
            wrmxpress_command_split,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        print("Running wrmXpress.")
        docker_output = []
        wells_analyzed = []
        wells_to_be_analyzed = len(wells)

        for line in iter(process.stdout.readline, ""):
            docker_output.append(line)
            file.write(line)
            file.flush()

            if "Generating w1 thumbnails" in line:
                output_path = Path(volume, "output", "thumbs", platename + ".png")
                while not os.path.exists(output_path):
                    time.sleep(1)

                fig_1 = create_figure_from_filepath(output_path)
                print("wrmXpress has finished.")
                docker_output.append("wrmXpress has finished.")
                docker_output_formatted = "".join(docker_output)

                return fig_1, False, False, "", f"```{docker_output_formatted}```"
    ```

- **Progress Tracking** 🚀:
  - After initiating the module, analyze the output logs to find specific progress indicators. Look for repeated elements that signal a new well is being analyzed or a well has finished being analyzed.
  - Sample code to detect and handle running wells:
    ```python
    elif "Running" in line:
        well_running = line.split(" ")[-1].strip()  # Use strip() to remove '\n'
        if well_running not in wells_analyzed:
            wells_analyzed.append(well_running)
            well_base_path = Path(
                volume,
                f"{platename}/TimePoint_1/{plate_base}_{well_running}",
            )
            # Use rglob with case-insensitive pattern matching for .TIF and .tif
            file_paths = list(
                well_base_path.parent.rglob(
                    well_base_path.name + "*[._][tT][iI][fF]"
                )
            )

            # Sort the matching files to find the one with the lowest suffix number
            if file_paths:
                file_paths_sorted = sorted(file_paths, key=lambda x: x.stem)
                # Select the first file (with the lowest number) if multiple matches are found
                img_path = file_paths_sorted[0]
            else:
                # Fallback if no matching files are found
                img_path = well_base_path.with_suffix(".TIF")  # Default to .TIF if no files found

            fig = create_figure_from_filepath(img_path)
            docker_output_formatted = "".join(docker_output)
            set_progress(
                (
                    str(len(wells_analyzed)),
                    str(wells_to_be_analyzed),
                    fig,
                    f"```{img_path}```",
                    f"```{docker_output_formatted}```",
                )
            )
    ```

- **Completion** 🏁:
  - Ensure that you return results only after the module's execution completes. This ensures that your GUI accurately reflects the status and results of the analysis.

### Contact for Queries 📬

- If you encounter issues or need clarification, please reach out to Zachary Caterer at `catererzt4830@uwec.edu`.

## Note on Combining Multiple Modules 📚🔗

The steps outlined above for adding a new module to your system are similarly applicable when you want to combine multiple modules. While the specific details might vary slightly depending on the modules you're integrating, the core process remains consistent:

1. **Module Configuration** 🎚️:
   - Adjust the module selection and settings in the same way, whether you are adding or combining modules.
   
2. **YAML and Environment Setup** 📐:
   - Ensure all involved modules are properly configured in the YAML files and that the environment setup accounts for multiple modules.

3. **Execution and Logging** 📝:
   - The execution logic, including subprocess management and logging, will need to accommodate all modules involved. Ensure that the process handles outputs and logs from multiple modules seamlessly.

4. **Progress Tracking and Feedback** 🔄:
   - Adjust the progress tracking to reflect the combined operations of the modules. This might involve aggregating data from multiple sources or handling more complex conditions during the execution.

### Integrating Multiple Modules 🧩

When combining multiple modules, consider the following additional steps:

- **Interdependencies** 🧬: Evaluate and handle any dependencies or conflicts between the modules. This might involve adjusting the execution order or modifying the modules to ensure compatibility.
- **Testing** 🔍: Rigorously test the combined functionality to identify and resolve any integration issues. This is crucial to ensure that the integrated modules operate smoothly and efficiently.
- **Documentation** 📄: Update all relevant documentation to reflect the combined module setup. This includes guides, user manuals, and system diagrams.

By following these guidelines, you can effectively manage the integration of multiple modules, leveraging the flexibility and power of modular design to enhance your research GUI’s capabilities. 🚀🌟
