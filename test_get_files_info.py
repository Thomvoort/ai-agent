from functions.get_files_info import get_files_info

def main():
    print("Results for current directory:")
    print(get_files_info("calculator", "."))
    print("Results for current directory:")
    print(get_files_info("calculator", "pkg"))
    print("Results for current directory:")
    print(get_files_info("calculator", "/bin"))
    print("Results for current directory:")
    print(get_files_info("calculator", "../"))
    
    
main()