'use strict';

/* Controllers */
angular.module('flotoApp', ['ui.bootstrap']);

function FlotoCtrl($scope, $http) {
    $scope.myInterval = -1;
    $http.get('/floto/api/events/test/tip?n=11').success(function(data) {
        $scope.images = data.photos;

        window.setInterval(function(){
            $http.get('/floto/api/events/test/new').success(function(data) {
                for(var photo in data.photos) {
                    $scope.images.push(data.photos[photo]);
                    $scope.images[1].active = true;
                    $scope.images.shift();                   
                }
            })
        }, 3000);
    });

    $scope.displayImage = function(image) {
        image.active = true;    
    }
}
