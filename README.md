# appendix-generator



## Usage

```bash
python3 generate_appendix.py --nmap nmap.xml --dehashed dehashed.json --template path/to/appendix.docx --output outputfile.docx
```
It's also possible to run this tool with multiple nmap/dehashed files. Also, both types of files are no longer required, so if there's a case where you just need to generate dehashed output, just omit the '-n' flag -- and vice versa. 

Example:

```bash
python3 generate_appendix.py --dehashed dehashed1.json dehashed2.json dehashed3.json --template /path/to/appendix.docx --output outputfile.docx
```

## Test Docs

To make testing easy, I've included a test nmap XML file and a sample dehashed JSON file in the 'TestDocs' directory. 

## Template

The template for this tool is named 'template.docx' and is located in the 'Template' directory. This tool will ***technically*** work with an existing report, but make sure to update the variables in GenerateAppendix.py to conform to your report style.  
