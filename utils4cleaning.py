import pandas as pd
import os
from boltons.setutils import IndexedSet

def run_str2date(date_str, input_format="mm/dd/yy", out_format = "dd/mm/yyyy"):
    if input_format == "mm/dd/yy":
        mm, dd, yyyy = [int(i) for i in date_str.split("/")]

        if yyyy < 100:
            if yyyy < 50:
                yyyy += 2000
            else:
                yyyy += 1900

        #
        # if max(mm) > 12:
        #     print(f"wrong input month format, the maximum month is {max(mm)}")
        #
        # if max(dd) < 11:
        #     print(f"possible wrong input day format, the maximum month is {max(dd)}")
        #
        # if len(yyyy) == 2:
        #     if yyyy < int(19)

        return f"{yyyy}{mm:02d}{dd:02d}"

def run_excel2csv(excel_path, output_dir="", log_path="", converters={'Date': str}, dtype=object):
    if len(log_path):
        f = open(log_path, "a+")
    else:
        f = 0
    print(excel_path)
    if len(output_dir):
        excel_path = os.path.basename(excel_path)

    sheets = pd.read_excel(excel_path, sheet_name=None, converters=converters, dtype=dtype) #read dates as string
    for t, s in enumerate(sheets):
        print(f"\t", t, "sheet: ", s)
        sheet_name = list(sheets.keys())[t]
        df = sheets[sheet_name]
        csv_path = os.path.join(f"{os.path.join(output_dir,excel_path)}_sheet_{sheet_name}.csv".replace(' ', '_'))
        df.to_csv(csv_path,index=False)
        if f:
            f.write(f"{excel_path}\n sheetname: {sheet_name}\n")
            f.write(str(df.head()))
            f.write(f"\nstored {csv_path}\n{'-' * 20}\n\n")
        print("\t\t", f"stored {csv_path}")

    if f:
        f.close()

def get_left_right(list_left, list_right):
    left = IndexedSet(list_left)
    right = IndexedSet(list_right)

    left_only = list(left - right)
    right_only = list(right - left)
    left_and_right = list(left | right)

    return left_and_right, left_only, right_only

if __name__ == '__main__':
    if 0:
        data_dir = "D:\\N\\10-prj\\00-data\\Spielberg\\"
        excel_paths = [p for p in os.listdir(data_dir+"ori") if p.endswith(".xlsx")]
        for p in excel_paths:
            run_excel2csv(data_dir+"ori\\"+p,  log_path=data_dir + "ori\\log.txt")

        csv_input_path = data_dir + "tableau-extract-budget-rating.csv"
        df = pd.read_csv(csv_input_path)
        df["Unadjusted Gross"] = df["Unadjusted Gross"].apply(lambda x: x[1:] )
        df["Release_yyyymmdd"] = df["Release"].apply(lambda x: run_str2date(x))
        df["Release_yyyy"] = df["Release_yyyymmdd"].apply(lambda x: int(x[:4]))
        assert (sum(df["Release_yyyy"] != df.Year)==0), "converted year is different"
        print(sorted(df["Release_yyyymmdd"].values))
        # for t,d in enumerate(df["Release"].values):
        #     print(t, run_str2date(d))

        # df["Release_yyyy"] = df["Release_yyyymmdd"].apply(lambda x: x.split("/")[0])
        # df["Release_mm"] = df["Release_yyyymmdd"].apply(lambda x: x.split("/")[1])
        # df["Release_dd"] = df["Release_yyyymmdd"].apply(lambda x: x.split("/")[-1])


        df.to_csv(csv_input_path[:-4] + "_01.csv", index=False)
        print(df.describe())

        k = 0


