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
                    if($scope.images[0].active === true) {
                        $scope.images[1].active = true;
                        window.setTimeout(function() {
                            $scope.images.push(data.photos[photo]);
                            $scope.images.shift();                           
                        }, 300);

                    } else {
                        $scope.images.push(data.photos[photo]);
                        $scope.images.shift();                       
                    }                 
                }
            })
        }, 5000);
    });

    $scope.displayImage = function(image) {
        image.active = true;    
    }
}
