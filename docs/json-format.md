# Metaphor JSON Format

The following is a description of the JSON that is acceptable to the
pipeline. `Parser_time`, `henry_time` and `parser_output` are not
updated in the repo as of now.

```
{
    "step": [1,2,3],
    # Denotes the last step that is to be processed; currently not
    # functional; default value is 3 to run the whole pipeline",

    "kb": string,
    # Takes the whole path to the LB or the name in the uploads directory;
    # default is None; this would load the default kb defined for each
    # language.

    "enableDebug": [True,False],
    # The debug option; default is false. set to true by the interface"

    "language": ["EN", "ES", "FA", "RU"],
    # Cannot be empty.

    "metaphorAnnotationRecords": [
        # Arrays of the sentences to process by the pipeline. The system
        # will add its response in JSON fields for each sentence.
        {
             "sentenceId": number,
             # Default is 1 and it keeps on incrementing if more than one
             # request in a single JSON.,

             "linguisticMetaphor": string,
             # Cannot be empty; it's the sentence to process.
        }
        ...
     ],

     "depth": number,
     # Max Henry depth; default is 3.

     "dograph": [True,False],
     # To generate graph even if no debug option; takes boolean value,
     # default is false. The graph is visible in the web interface, log
     tab.

     "extractor": string,
     # Select which CM extractor file to use; default is
     # 'extractor-no-soan-june-2014-eval'",

     "parser_time": "if present, populates the value in the response json
     with the parser processing time",

     "henry_time": "if present, populates the value in the response json
     with the henry processing time",

     "parser_output": "if present with null value: the system will assign
     to it the output of the LF generator. if present with value: the
     system will skip the parser and use the value as input to henry. If
     not present: nothing is done."
}
```
