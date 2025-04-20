import sqlite3
import pandas as pd
import numpy as np
import os
import logging
os.chdir(r"G:\Codecademy\Projects\subscriber_pipeline\dev")

logging.basicConfig(filename='cleaned_db.log', format='%(asctime)s - %(levelname)s - %(message)s', filemode='w', level=logging.DEBUG, force=True)
logger = logging.getLogger(__name__)

def student_table_cleaning(df):
    now = pd.to_datetime("now")
    df["age"] = (now - pd.to_datetime(df['dob'])).dt.days // 365
    df['contact_info'] = df['contact_info'].apply(lambda x: eval(x))
    expanded = pd.json_normalize(df['contact_info'])
    df = pd.concat([df.drop('contact_info', axis=1), expanded], axis=1)
    mailing_address_split = df.mailing_address.str.split(',', expand=True)
    mailing_address_split.columns = ['street', 'city', 'state', 'zipcode']
    df = pd.concat([df.drop('mailing_address', axis=1), mailing_address_split], axis=1)
    df['job_id'] = df['job_id'].astype(float)
    df['num_course_taken'] = df['num_course_taken'].astype(float)
    df['current_career_path_id'] = df['current_career_path_id'].astype(float)
    df['time_spent_hrs'] = df['time_spent_hrs'].astype(float)
    course_taken_missing = df[df[['num_course_taken']].isnull().any(axis=1)]
    missing_data = pd.DataFrame()
    missing_data = pd.concat([missing_data, course_taken_missing])
    df = df.dropna(subset=['num_course_taken'])
    career_path_missing = df[df[['current_career_path_id']].isnull().any(axis=1)]
    df.loc[:, ['current_career_path_id', 'time_spent_hrs']] = df[['current_career_path_id', 'time_spent_hrs']].fillna(0)
    job_id_missing = df[df[['job_id']].isnull().any(axis=1)]
    missing_data = pd.concat([missing_data, job_id_missing])
    df = df.dropna(subset=['job_id'])
    return(df, missing_data)

def courses_table_cleaning(df):
    no_career_path = {'career_path_id' : 0, 'career_path_name' : 'No courses currently', 'hours_to_complete' : 0}
    df.loc[len(df)] = no_career_path
    return(df)

def student_jobs(df):
    return(df.drop_duplicates())

def test_nulls(df):
    df_missing = df[df.isnull().any(axis=1)]
    count_missing = len(df_missing)

    try:
        assert count_missing == 0, 'There are ' + str(count_missing) + 'nulls'
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('No null rows')

def test_schema(local_df, db_df):
    errors = 0
    for col in db_df:
        try:
            if local_df[col].dtypes != db_df[col].dtypes:
                errors += 1
        except NameError as ne:
            logger.exception(ne)
            raise ne
    if errors > 0:
        assert_error_msg = str(errors) + ' column dtypes arent the same'
        logger.exception(assert_error_msg)
    assert errors== 0, assert_error_msg

def test_column_amount(local_df, db_df):
    try:
        assert len(local_df.columns) == len(db_df.columns)
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('column amount same')

def path_id_test(students, courses):
    student_table = students.current_career_path_id.unique()
    is_in = np.isin(student_table, courses.career_path_id.unique())
    missing = student_table(~is_in)
    try:
        assert len(missing) == 0, 'Missing ' + str(list(missing)) + 'in career_paths'
    except AssertionError as ae:
        logger.exception(ae)
        raise ae
    else:
        print('All career_path_id are present')

def job_id_test(students, student_jobs):
        student_table = students.job_id.unique()
        is_in = np.isin(student_table, student_jobs.job_id.unique())
        missing = student_table(~is_in)
        try:
            assert len(missing) == 0, 'Missing ' + str(list(missing)) + 'in job_id'
        except AssertionError as ae:
            logger.exception(ae)
            raise ae
        else:
            print('All job_ids are present')

def main():
    logger.info('Start log')

    with open('changelog.md', 'a+') as f:
        lines = f.readlines()
    if len(lines) == 0:
        next_ver = 0
    else:
        next_ver = intlines([0].split(',')[2][0])+1

    con = sqlite3.connect('cademycode.db')
    students = pd.read_sql_query("SELECT * FROM cademycode_students", con)
    courses = pd.read_sql_query("SELECT * FROM cademycode_courses", con)
    student_jobs = pd.read_sql_query("SELECT * FROM cademycode_student_jobs", con)
    con.close()

    try:
        con = sqlite3.connect('cademycode.db')
        students = pd.read_sql_query("SELECT * FROM cademycode_students", con)
        courses = pd.read_sql_query("SELECT * FROM cademycode_courses", con)
        student_jobs = pd.read_sql_query("SELECT * FROM cademycode_student_jobs", con)
        con.close()

        new_students = students[~np.isin(students.uuid.unique(), clean_db.uuid.unique())]
    except:
        new_students = students
        clean_db = []
    clean_new_students, missing_data = student_table_cleaning(new_students)

    try:
        new_missing_data = missing_data[~np.isin(missing_data.uuid.unique(), missing_db.uuid.unique())]
    except:
        new_missing_data = missing_data
    
    if len(new_missing_data) > 0:
        connection = sqlite3.connect('cleansed_cademycode_data.db')
        missing_data.to_sql('missing_data', connection, if_exists='append', index=False)
        connection.close()
    if len(clean_new_students) > 0:
        clean_career_paths = courses_table_cleaning(courses)
        clean_student_jobs = student_table_cleaning(student_jobs)

        job_id_test(clean_new_students, clean_student_jobs)
        path_id_test(clean_new_students, clean_career_paths)

        df_clean = clean_new_students.merge(clean_career_paths, left_on='current_career_path_id', right_on='career_path_id', how='left')
        df_clean = df_clean.merger(clean_student_jobs, on='job_id', how='left')

        if len(clean_db) > 0:
            test_column_amount(df_clean, clean_db)
            test_schema(df_clean, clean_db)
            test_nulls(df_clean)
        
        connection = sqlite3.connect('cademycode_cleansed.db')
        df_clean.to_sql('joined_cademycode', connection, if_exists='append', index=False)
        clean_db = pd.read_sql_query('SELECT * FROM joined_cademycode', con)
        connection.close()

        clean_db.to_csv('cleansed-cademycode.csv')

        new_lines = [
            '## 0.0' + str(next_ver) + '### Added\n' + '\n'
            '_ ' + str(len(df_clean)) + '\n'
            '_ ' + str(len(new_missing_data)) + 'new_missing_data'
        ]
        w_lines = ''.join(new_lines + lines)
        with open('changelog.md', 'w') as f:
            for line in w_lines:
                f.write(line)
    else:
        print('no new data')
        logger.info('End')

if __name__ == '__main__':
    main()