'use strict';

/* Controllers */

function FlotoCtrl($scope, $http) {
	$http.get('phones/phones.json').success(function(data) {
		$scope.phones = data;
		console.log(data);
	});
}
