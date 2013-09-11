function loginCtrl($scope, $http, $location) {
    $scope.username = "";
    $scope.password = "";
    console.log('$scope.username : ' + $scope.username);

    $scope.login = function() {
        if(this.username) {
            $scope.username = this.username;
            var login_data = 'username=' + this.username + '&password=' + this.password;

            $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
            $http.post('/login',  login_data).
                success(function(data, status) {
                    window.location = '/';
                }).
                error(function(data, status) {
                    console.log('edata : ' + data);
            });
        }
    };

    $scope.logout = function() {
        $http.get('/logout').
            success(function(data, status) {
                window.location = '/';
            }).
            error(function(data, status) {
                console.log('edata : ' + data);
        });
    };
}
