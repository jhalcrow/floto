'use strict';

/* Controllers */
angular.module('flotoApp', ['ui.bootstrap']);


function FlotoCtrl($scope, $http) {
    $scope.myInterval = 30000;
    $http.get('/floto/api/events/test/tip?n=11').success(function(data) {
        $scope.images = data.photos;
        console.log(data);
        window.setInterval(function(){
            $http.get('/floto/api/events/test/new').success(function(data) {
                for(var photo in data.photos) {
                    $scope.images.unshift(data.photos[photo]);
                    $scope.images.pop();                   
                }
            })
        }, 5000);
    });

    $scope.displayImage = function(image) {
        image.active = true;    
    }
}
