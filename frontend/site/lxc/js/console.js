$(document).ready(function() {
    var term = null;
    var sock = null;


    function setupConsole(id) {
        var element = document.getElementById('lxc_console');
        var cell = createCell(element);
        var size = getSize(element, cell);

        var height = Math.max(Math.round(window.innerHeight / 25), 15);
        var width = size.cols - 1;

        sock = new WebSocket(
          endpoint+"/1.0/console?id="+
          id+"&width="+width+"&height="+height+"&compute_node="+
          compute_node+"&auth="+os_token+"&uuid="+instance_id+"&tenant_id="+tenant_id);
        sock.onopen = function (e) {
            term = new Terminal({
                cols: width,
                rows: height,
                useStyle: true,
                screenKeys: false
            });

            $('#lxc_console_reconnect').css("display", "none");
            term.open(document.getElementById("lxc_console"))

            term.on('data', function(data) {
                sock.send(data);
            });

            sock.onmessage = function(msg) {
                term.write(msg.data);
            };

            sock.onclose = function(msg) {
                term.destroy();
                $('#lxc_console_reconnect').css("display", "inherit");
            };
        };
    }

    function getSize(element, cell) {
        var wSubs   = element.offsetWidth - element.clientWidth,
            w       = element.clientWidth - wSubs,

            hSubs   = element.offsetHeight - element.clientHeight,
            h       = element.clientHeight - hSubs,

            x       = cell.clientWidth / 21,
            y       = cell.clientHeight,

            cols    = Math.max(Math.floor(w / x), 10),
            rows    = Math.max(Math.floor(h / y), 10),

            size    = {
                cols: cols,
                rows: rows
            };

        return size;
    }

    function createCell(element) {
        var cell            = document.createElement('div');

        cell.innerHTML = 'root@lxc-session:~#';
        cell.id = "lxc_console_measurement";

        element.appendChild(cell);

        return cell;
    }


    setupConsole(id);

});
