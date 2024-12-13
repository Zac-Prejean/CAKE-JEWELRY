
PrintLayoutLab

This code is a Python script that creates a web application called "Print Layout Lab" using the Flask web framework. It imports various configurations, such as SKU prefixes and lists of valid SKUs for different product types. The main purpose of this application is to process and export images with personalized text based on the data from a CSV file. The script imports several libraries and configuration files to achieve this. Users can then export the images in a specified format.

Precheck Editor -

  * When a user selects a CSV file, the script reads and parses it using the Papa Parse library. It then displays a table preview of the parsed CSV data with input fields for personalization. Users can modify these fields, and when they click the save button, the script updates the CSV data with the changes and downloads the updated file.

  * The main functions in the script handle file input events, extract personalization text from the item options, and generate an HTML table based on the CSV data. The script also has event listeners for actions like displaying a preview, saving changes, and updating the CSV data.

Designer -

    The application processes the text for personalization by applying special rules and skipping certain lines. It loads a font from a given font path and font size, and determines the font path based on the given SKU. It calculates the font size and placement based on the SKU and number of characters and handles the second line of text if needed. Additionally, it creates an error image with a "Reupload to PreCheck" message when required and draws a white background behind the text if needed.

  * The script processes each row from the input dataframe and generates an image with personalized text. It then exports images for each row in the given dataframe. A generator function is used to process the rows of the input CSV data and yield progress messages.

  * The Flask web application has several routes and views, including a home page, PreCheck page, Designer page, and TemplateMerger page. The main route processes the input CSV file and generates images with personalized text based on the data. The images are saved in a folder located in the user's "Downloads" directory. The output images have text added based on the product's SKU, font, font size, and placement information, with special rules and font color processing applied.

Template Merger -

  * Also allows users to change the output format by clicking on different format options.

  * The script generates a canvas element with the combined PNGs. The images are drawn on the canvas with the desired width and height. The canvas is then converted to a data URL, which is further converted to a Blob for downloading the final image.

