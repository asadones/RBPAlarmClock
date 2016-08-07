'use strict';

angular.module('AlarmClock.weather', [
])

  .factory('CurrentWeather', ['$resource',
    function ($resource) {
      return $resource('/weather/current');
    }])

  .factory('WeatherForecast', ['$resource',
    function ($resource) {
      return $resource('/weather/forecast');
    }])

  .controller('CurrentWeatherCtrl', ['$scope', '$timeout', 'CurrentWeather',
    function ($scope, $timeout, CurrentWeather) {

      function refreshWeather () {
        CurrentWeather.get(
          {'units': 'metric'},
          function (response) {
            $scope.weather = response;
            $timeout(refreshWeather, 300000);
          }, function () {
            $scope.weather = {'status': 'error', 'code': '?'};
            $timeout(refreshWeather, 300);
          }
        );
      }

      // Start Weather Widget
      refreshWeather();
    }])

  .controller('WeatherForecastCtrl', ['$scope', '$timeout', 'WeatherForecast',
    function ($scope, $timeout, WeatherForecast) {

      function refreshForecast () {

        function buildItem (item) {
          return {
            date: new Date(item.timestamp * 1000),
            icon: item.icon,
            temperature: item.temperature,
            label: item.label
          };
        }

        WeatherForecast.get(
          {'units': 'metric'},
          function (response) {
            $scope.forecast = [
              buildItem(response.forecast[0]),
              buildItem(response.forecast[1]),
              buildItem(response.forecast[2])
            ];
            $timeout(refreshForecast, 3600000);
          }, function () {
            $scope.forecast = {'status': 'error', 'code': '?'};
            $timeout(refreshForecast, 30000);
          }
        );
      }

      // Start Weather Widget
      refreshForecast();
    }]);
