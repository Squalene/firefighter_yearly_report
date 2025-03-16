## Dependencies

### Install UV (package dependency manager)

```curl -LsSf https://astral.sh/uv/install.sh | sh```

### Install weasyprint (HTML -> PDF)

```brew install weasyprint```


## How to run

Open ```src/main.py``` and make sure that the global variables are correct.  
With a terminal located at the root of the project: 
- Run ```uv sync```  
- Run ```uv run src/main.py```  

The outcome will be stored in the **output** folder