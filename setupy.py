import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/assets/coelho.2.ico") ]
cx_Freeze.setup(
    name = "Jardim Secreto",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["recursos"]
        }
    }, executables = executaveis
)    