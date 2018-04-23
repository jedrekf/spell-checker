<?php

function router($httpMethods, $route, $callback, $exit = true)
{
    static $path = null;
    if ($path === null) {
        $path = parse_url($_SERVER['REQUEST_URI'])['path'];
        $scriptName = dirname(dirname($_SERVER['SCRIPT_NAME']));
        $scriptName = str_replace('\\', '/', $scriptName);
        $len = strlen($scriptName);
        if ($len > 0 && $scriptName !== '/') {
            $path = substr($path, $len);
        }
    }
    if (!in_array($_SERVER['REQUEST_METHOD'], (array) $httpMethods)) {
        return;
    }
    $matches = null;
    $regex = '/' . str_replace('/', '\/', $route) . '/';
    if (!preg_match_all($regex, $path, $matches)) {
        return;
    }
    if (empty($matches)) {
        $callback();
    } else {
        $params = array();
        foreach ($matches as $k => $v) {
            if (!is_numeric($k) && !isset($v[1])) {
                $params[$k] = $v[0];
            }
        }
        $callback($params);
    }
    if ($exit) {
        exit;
    }
}

$SC = new SoapClient("http://www.spolszcz.pl/webapi.wsdl");


// Default index page
router('GET', '^/$', function() {
    echo '<p>Microservice documentation at <a href="https://github.com/jedrekf/spell-checker"> Spell-checker documentation</a></p>';
});

router('POST', '^/spolszcz$', function() {
    global $SC;
    header('Content-Type: application/json');
    $json = json_decode(file_get_contents('php://input'), true);
    echo $SC->Spolszcz($json["sentence"]);
});


header("HTTP/1.0 404 Not Found");
echo '404 Not Found';