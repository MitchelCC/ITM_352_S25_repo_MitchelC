survey_years = (1980,1982,  1983, 1984, 1985, 1986, 1987, 1988, 1989)
respondents = (17, 35, 26, 26, 25, 27, 35, 21, 19)

years_list = []
respondents_list = []

for year, respondent in zip(survey_years, respondents):
    years_list.append(year)
    respondents_list.append(respondent)

survey_data = {
    "years": years_list,
    "respondents": respondents_list
}

print(survey_data)