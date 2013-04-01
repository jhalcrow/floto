'use strict';

/* Controllers */
angular.module('flotoApp', ['ui.bootstrap']);


function FlotoCtrl($scope, $http) {
    $scope.myInterval = 30000;
    $http.get('/events/test/tip').success(function(data) {
        $scope.images = data.photos;
        console.log(data);
        window.setInterval(function(){
            $http.get('/events/test/new').success(function(data) {
                for(var photo in data.photos) {
                    $scope.images.shift();
                    $scope.images.push(data.photos[photo]);                   
                }
            })
        }, 5000);
    });


/*
    $scope.displayImage = function(image) {
        while($scope.images.indexOf(image) !== 0) {
            console.log($scope.images);
            var tempImage = $scope.images[0];
            $scope.images.shift();
            $scope.images.push(tempImage);
        }
        image.active = true;    
        console.log("IMAGE");
    }*/
}
