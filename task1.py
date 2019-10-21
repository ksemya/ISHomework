import numpy as np
from numpy import genfromtxt
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get


def getResults(user_id):
	users = getUserData('data.csv')
	context_day = getMovieData('context_day.csv')
	context_place = getMovieData('context_place.csv')

	similarUsers = getSimilarUsers(users, user_id)
	orderedMovies = getRating(similarUsers, users, user_id)

	recomendedMovies = getRecommendation(orderedMovies, 3, context_day, context_place, ['Sun', 'Sat'], ['h'])

	movieRatings = {}
	for i in orderedMovies:
		movieRatings["Movie " + str(i)] = orderedMovies[i]


    # getting only first recommended movie!

	recommendedMovie = next(iter(recomendedMovies))

	result = {
        "user": user_id,
        "1": movieRatings,
        "2": recomendedMovies
    }

	with open('Ksenia_Miakinkaia.json', 'w') as file:
		json.dump(result, file)
	file.close()
	print("File for user 12 created!")


def getUserData(fileName):

    data = genfromtxt(fileName, delimiter=', ', dtype=str)
    row = data.shape[0]
    users = {}

    for i in range(row - 1):
        currentItem = data[i + 1][1:]
        for j in range(currentItem.shape[0]):
            if int(currentItem[j]) == -1:
                currentItem[j] = 0
        users[i + 1] = np.array(currentItem, dtype=int)

    return users


def getMovieData(file_name):

    data = genfromtxt(file_name, delimiter=', ', dtype=str)
    row = data.shape[0]
    column = data.shape[1]
    movies = {}

    for i in range(row - 1):
        for j in range(column - 1):
            if data[i + 1][j + 1] != '-1':
                if (j+1) in movies:
                    movies[j+1] = np.append(movies[j+1], data[i+1][j+1])
                else:
                    movies[j+1] = np.array([data[i+1][j+1]])

    return movies


def getSimilarUsers(users, selected_user_id):

    knn = 4
    similarityData = {}
    for currentId in users:
        if currentId != selected_user_id:
            comp = np.array([])
            sqCurrent = np.array([])
            sqSelected = np.array([])
            for movie in range(users[currentId].shape[0]):
                if users[currentId][movie] > 0 and users[selected_user_id][movie] > 0:
                    comp = np.append(comp, users[currentId][movie]*users[selected_user_id][movie])
                    sqCurrent = np.append(sqCurrent, users[currentId][movie] ** 2)
                    sqSelected = np.append(sqSelected, users[selected_user_id][movie] ** 2)
            comp = np.sum(comp)
            sqCurrent = np.sum(sqCurrent) ** 0.5
            sqSelected = np.sum(sqSelected) ** 0.5
            metric = (sqCurrent * sqSelected)
            metric = comp / metric
            similarityData[currentId] = metric
    similarityData = sorted(similarityData.items(), key=lambda item: -item[1])
    return similarityData[:knn]


def getAvg(currentList):
    listSum = 0
    count = 0
    for i in range(len(currentList)):
        if currentList[i] != 0:
            listSum += currentList[i]
            count += 1
    return listSum / count


def getRating(similarUsers, users, selectedUser):

    resultRatings = {}
    selectedUserData = users[selectedUser]
    avgRating = getAvg(selectedUserData)

    for movieId in range(len(selectedUserData)):
        movieRating = selectedUserData[movieId]
        if movieRating == 0:
            dividend = np.array([])
            divider = np.array([])
            for user in similarUsers:
                currentUserId = user[0]
                currentUserData = users[currentUserId]
                if currentUserData[movieId] > 0:
                    avgRatingCurrent = getAvg(currentUserData)
                    dividend = np.append(dividend, user[1] * (currentUserData[movieId] - avgRatingCurrent))
                    divider = np.append(divider, user[1])
            dividend = np.sum(dividend)
            divider = np.sum(divider)
            resultsRating = avgRating + (dividend/divider)
            resultRatings[movieId+1] = round(resultsRating, 3)

    return resultRatings


def getRecommendation(movies, borderRating, contextDayData, contextPlaceData, currentContextDay, currentContextPlace):

    bestMovies = {}

    for i in movies:
        if movies[i] >= borderRating:
            contextDay = contextDayData[i]
            contextPlace = contextPlaceData[i]
            contextDayRating = 0
            contextPlaceRating = 0
            for j in range(len(contextDay)):
                if any(x == contextDay[j] for x in currentContextDay):
                    contextDayRating += 1
            for k in range(len(contextPlace)):
                if any(x == contextPlace[k] for x in currentContextPlace):
                    contextPlaceRating += 1
            bestMovies[i] = (contextDayRating / len(contextDay)) * (contextPlaceRating / len(contextPlace))

    maxRating = max(bestMovies.values())
    resultMovies = {}

    for v in movies:
        if v in bestMovies and bestMovies[v] == maxRating:
            resultMovies["Movie " + str(v)] = str(movies[v]) + " (+" + str(round(maxRating, 3)) + ")"

    return resultMovies

if __name__ == "__main__":
    getResults(12)

