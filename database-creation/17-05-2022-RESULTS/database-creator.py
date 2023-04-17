import json
import csv
import sys

def issue_exists(listOfElems, elem):
    if listOfElems.count(elem) > 0:
        return True
    else:
        return False

def duplicate_exists(issues_list):
    for issue in issues_list:
        if issues_list.count(issue) > 1:
            print(issue[0])
            print("DUPLICATE EXIST IN ISSUES LIST")

def duplicate_remove(issues_list):
    for issue in issues_list:
        if issues_list.count(issue) > 1:
            issues_list.remove(issue)
    return issues_list

def duplicate_remove_from_all_lists(common_list, bugs, enhancements, questions):
    for issue in common_list:
        if common_list.count(issue) > 1:
            if bugs.count(issue) > 0:
                bugs.remove(issue)
            if enhancements.count(issue) > 0:
                enhancements.remove(issue)
            if questions.count(issue) > 0:
                questions.remove(issue)
            while common_list.count(issue) > 0:
                common_list.remove(issue)

    return common_list, bugs, enhancements, questions

#вводим ограничение на максимальное число символов в ячейке для того, чтобы не получить ошибку о превышении, т.к. некоторые поля будут больше
csv.field_size_limit(sys.maxsize)
file_date = "2022-05-17-14-17-51"
with open(f"{file_date}-issues.csv", newline='', encoding='utf-8') as file_issues:
    all_issues = csv.reader(file_issues)
    # конвертация в список для того, чтобы работала функция len() в конце
    all_issues = list(all_issues)
    issues_with_labels = []
    # all_issues_labeled_dataset - датасет с issue, которые принадлежат одной из трех категорий bug, enhancements, question
    all_issues_labeled_dataset = []
    issues_bugs = []
    issues_enhancements = []
    issues_questions = []
    #удаляем дубликаты в списке всех issues
    all_issues = duplicate_remove(all_issues)
    for issue in all_issues:
        labels = issue[3]
        try:
            labels = json.loads(labels)
            if len(labels):
                issues_with_labels.append(issue)
                labels_removed = False
                for label in labels:
                    if label['name'] == "type: bug" or label['name'] == "blocking":
                        issueExist = issue_exists(issues_bugs, issue)
                        #проверка на дубликаты
                        if issueExist:
                            pass
                        else:
                            del issue[3]
                            issue.append('bug')
                            issues_bugs.append(issue)
                            all_issues_labeled_dataset.append(issue)

                    elif label['name'] == "type: feature" or label['name'] == "type: enhancement":
                        issueExist = issue_exists(issues_enhancements, issue)
                        if issueExist:
                            pass
                        else:
                            del issue[3]
                            issue.append('enhancement')
                            issues_enhancements.append(issue)
                            all_issues_labeled_dataset.append(issue)

                    elif label['name'] == "type: question":
                        issueExist = issue_exists(issues_questions, issue)
                        if issueExist:
                            pass
                        else:
                            del issue[3]
                            issue.append('question')
                            issues_questions.append(issue)
                            all_issues_labeled_dataset.append(issue)

            else:
                pass

        #данная ошибка свидетельствует о том, что в полученном списке issues первой строкой идут названия полей
        except Exception as e: print(e)

    all_issues_labeled_dataset, issues_bugs, issues_enhancements, issues_questions = duplicate_remove_from_all_lists(all_issues_labeled_dataset, issues_bugs, issues_enhancements, issues_questions)


print("ALL ISSUES",len(all_issues))
print("ISSUES WITH LABELS",len(issues_with_labels))
print("ISSUES WITH LABELS BUG, ENHANCEMENT, QUESTION",len(all_issues_labeled_dataset))
print("ISSUES BUGS",len(issues_bugs))
print("ISSUES ENHANCEMENTS",len(issues_enhancements))
print("ISSUES QUESTIONS",len(issues_questions))
#проверка на дубликаты
duplicate_exists(issues_bugs)
duplicate_exists(issues_enhancements)
duplicate_exists(issues_questions)
duplicate_exists(all_issues_labeled_dataset)

with open(f"{file_date}-ALL-LABELED-LIST.csv", 'w') as bugs_file:
    write = csv.writer(bugs_file)
    write.writerows(all_issues_labeled_dataset)

with open(f"{file_date}-BUGS-LIST.csv", 'w') as bugs_file:
    write = csv.writer(bugs_file)
    write.writerows(issues_bugs)

with open(f"{file_date}-ENHACEMENTS-LIST.csv", 'w') as enhancements_file:
    write = csv.writer(enhancements_file)
    write.writerows(issues_enhancements)

with open(f"{file_date}-QUESTIONS-LIST.csv", 'w') as questions_file:
    write = csv.writer(questions_file)
    write.writerows(issues_questions)
