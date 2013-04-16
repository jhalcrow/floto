'use strict';

/* Controllers */
angular.module('flotoApp', ['ui.bootstrap']);

function FlotoCtrl($scope, $http) {
    $scope.myInterval = 3000;
    $http.get('/floto/api/events/test/tip?n=11').success(function(data) {
        $scope.images = data.photos;

        window.setInterval(function(){
            $http.get('/floto/api/events/test/new').success(function(data) {
                for(var photo in data.photos) {
                    console.log($scope.images[0]);
                    if($scope.images[$scope.images.length].active === false) {
                        $scope.images.unshift(data.photos[photo]);
                        $scope.images.pop();                   
                    }
                }
            })
        }, 6000);
    });

    $scope.displayImage = function(image) {
        image.active = true;    
    }
}
