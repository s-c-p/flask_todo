function loginCrtl($scope, $http, $location) {
    $scope.username = "";
    $scope.password = "";

    $scope.login = function() {
        if(this.username) {
            console.log('this.username : ' + this.username);
            var login_data = 'username=' + this.username + '&password=' + this.password;

            $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
            $http.post('/login',  login_data).
                success(function(data, status) {
                    console.log(data);
                    window.location = '/';
                    console.log('data');
                }).
                error(function(data, status) {
                    console.log('edata : ' + data);
            });
        }
    };
}
