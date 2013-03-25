'use strict';

/* Controllers */
angular.module('flotoApp', ['ui.bootstrap']);


function FlotoCtrl($scope, $http) {
    $scope.myInterval = 30000;
    $http.get('pokemon.json').success(function(data) {
        $scope.images = data;
        console.log(data);
    });

    $scope.displayImage = function(image) {
        while($scope.images.indexOf(image) !== 0) {
            console.log($scope.images);
            var tempImage = $scope.images[0];
            $scope.images.shift();
            $scope.images.push(tempImage);
        }
        image.active = true;    
        console.log("IMAGE");
    }
}
