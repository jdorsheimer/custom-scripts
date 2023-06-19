# Define a function to remove comments from an R script
remove_comments <- function(input_file, output_file) {
  
  # Use the readLines function to read the content of the input_file.
  # This function reads text line by line and returns a character vector where each element represents a line in the file.
  lines <- readLines(input_file)
  
  # Use the lapply function to apply a function to each line in the 'lines' character vector.
  # The function that is being applied is defined using an anonymous function with 'x' as the input (representing a line of text).
  uncommented_lines <- lapply(lines, function(x) {
    # Use the strsplit function to split each line at the comment symbol '#'.
    # The result of strsplit is a list, where each element is a character vector of the split components.
    # By using [[1]][1], we only keep the first part of the split (i.e., the code before the comment).
    code_part <- strsplit(x, "#")[[1]][1]
    
    # Check whether the code part is not NA, not an empty string, and not just white space.
    # If the code part meets these conditions (i.e., there is some code in this line), return it.
    # Otherwise, if the line is empty or contains only a comment, return NULL.
    # The trimws function is used to remove leading and trailing white spaces.
    # The nchar function is used to count the number of characters in a string (after white space removal in this case).
    if (!is.na(code_part) && code_part != "" && nchar(trimws(code_part)) > 0) {
      return(code_part)
    } else {
      return(NULL)
    }
  })
  
  # Use the unlist function to convert the 'uncommented_lines' list into a character vector.
  # NULLs (which represent lines that were only comments or white spaces) are automatically removed in this step.
  uncommented_lines <- unlist(uncommented_lines)
  
  # Use the writeLines function to write the uncommented code to the output_file.
  # This function writes each element of the 'uncommented_lines' character vector as a line in the file.
  writeLines(uncommented_lines, output_file)
  
}

# Test the function by removing comments from the test-flow_dbs.R script and writing the uncommented code to the test-flow_dbs_uncommented.R script.
remove_comments("/home/justin_dorsheimer/Scripts/test-flow_dbs.R", "/home/justin_dorsheimer/Scripts/test-flow_dbs_uncommented.R")
