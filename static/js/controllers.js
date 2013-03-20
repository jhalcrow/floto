'use strict';

/* Controllers */

function FlotoCtrl($scope, $http) {
	$http.get('pokemon.json').success(function(data) {
		$scope.phones = data;
		console.log(data);
	});
}
