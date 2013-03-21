'use strict';

/* Controllers */
angular.module('flotoApp', ['ui.bootstrap']);


function FlotoCtrl($scope, $http) {
	$scope.myInterval = 30000;
	$http.get('pokemon.json').success(function(data) {
		$scope.images = data;
		console.log(data);
	});
}
