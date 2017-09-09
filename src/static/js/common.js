$(document).ready(function() {


  function createGraph(array) {
    graphValues    = [],
    graphFrequency = 2403.47;

    for(var i = 0; i < 256; i++) {
      graphValues.push([graphFrequency.toFixed(4), array[i]]);
      graphFrequency += 0.2864;
      if(graphFrequency >= 2476.502) {
        graphFrequency = 2403.47;
      };
    }

    return graphValues;
  };


  var options = {
    xaxis: {
      min: 2403.47,
      max: 2476.502,
      tickSize: 12
    },
    yaxis: {
      min: -110,
      max: -20,
    },
    grid: {
      borderWidth: 1,
      color: '#999',
    },
    shadowSize: 0,
  },
  colors           = ['#EDC240', '#AFD8F8', '#CB4B4B', '#4DA74D', '#9440ED', '#BD9B33', '#8CACC6', '#FF5C2D', '#FF9999', '#66FF33'],
  colorsCopy       = [],
  hideDeviceGraph  = [],
  clientNames      = {},
  checkConnection  = '';


  // initialize web socket connection
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);


  // function for processing received data
  socket.on('get_show_data', function(data) {

    // if json object is incorrect
    try {
      var package = JSON.parse(data.data);
    } catch(e) {
      console.log(e.toString());
      return true
    }

    // client's data variables
    var clientIP,
        clientClassIP,
        clientPackage,
        clientDOM,
        deviceCounter = 0,

        // client's device data variables
        port   = [],
        serial = [],
        number = [],
        time   = [],
        signal = [];

    // extract client's data
    for(key in package) {
      clientIP      = key;
      clientClassIP = key.replace(/\./g, '-');
      clientPackage = package[key];
      clientDOM     = '.client.' + clientClassIP
    }

    // extract client's device data
    for(key in clientPackage) {
      port.push(key);
      serial.push(clientPackage[key].serial);
      number.push(clientPackage[key].number);
      time.push(clientPackage[key].time);
      signal.push(createGraph(clientPackage[key].values.split(',')));

      deviceCounter += 1;
    }

    // append new client. If it alredy exists, refresh device counter and client's name
    if($('.client-list > li').hasClass(clientClassIP)) {
      $(clientDOM + ' .client-info .info span:nth-child(2) span').html(deviceCounter);
      $(clientDOM + ' .client-info .name span').html(clientNames[clientClassIP]);
    } else {
      var clientNumber = $('.client-list > li').length + 1;

      for(var i = 0; i < deviceCounter; i++) {
        hideDeviceGraph.push(0);
      }

      $('ul.client-list').append(
        '<li class="client ' + clientClassIP + ' animated fadeInRight">' +
          '<div class="client-info">' +
            '<div class="name">' +
              '<span>Client ' + clientNumber + '</span>' +
              '<input type="text">' +
            '</div>' +
            '<div class="pause-block"><span>Paused</span></div>' +
            '<div class="pause-button"><i class="fa fa-pause" aria-hidden="true"></i></div>' +
            '<div class="info">' +
              '<span><i class="fa fa-user" aria-hidden="true"></i> ' + clientIP + '</span>' +
              '<span><i class="fa fa-microchip" aria-hidden="true"></i><span>' + deviceCounter + '</span></span>' +
            '</div>' +
          '</div>' +
          '<div class="client-device"><ul></ul></div>' +
        '</li>'
      );

      // pause handler
      $(clientDOM + ' .pause-button i').on('click', function() {
        if($(this).hasClass('fa-pause')) {
          socket.emit('get_send_command', [clientIP, 'pause']);
        } else {
          socket.emit('get_send_command', [clientIP, 'work']);
        }
      });

      // name setup handler
      $(clientDOM + ' .name span').on('click', function() {
        $(this).addClass('disable');
        $(this).next().addClass('active');
      });

      $(clientDOM + ' .name input').on('change', function() {
        if($(this).val() == '') {
          return true
        } else {
          socket.emit('get_client_name', [clientClassIP, $(this).val()]);
          clientNames[clientClassIP] = $(this).val();
          $(this).prev().html($(this).val());
          $(this).removeClass('active');
          $(this).prev().removeClass('disable');
        }
      });
    }

    // for first client add class active
    if(!$('ul.client-list > li').hasClass('active')) {
      $('ul.client-list > li:first-child').addClass('active');
    }

    // disable start window
    $('.start-window').removeClass('fadeOutLeft').addClass('animated fadeOutLeft');

    // if client has class active show his device data and graph
    if($(clientDOM).hasClass('active')) {
      $(clientDOM + ' .client-device ul').empty();
      for(var i = 0; i < deviceCounter; i++) {
        $(clientDOM + ' .client-device ul').append(
          '<li>' +
            '<span style="color:' + colors[i] + '">' + port[i] + '</span>' +
            '<span class="num">' + serial[i] + '</span>' +
            '<span class="num">' + number[i] + '</span>' +
            '<span class="num">' + time[i] + '</span>' +
          '</li>'
        );
      }

      for(var i = 0; i < hideDeviceGraph.length; i++) {
        if(hideDeviceGraph[i]) {
          signal[i] = [0, 0];
        }
      }

      $.plot('#graph', signal, options);
    }

    // client's window toggle
    $('ul.client-list .client').on('click', function() {
      if($(this).hasClass('active')) {
        return true
      } else {
        hideDeviceGraph = [];
        $('ul.client-list .client').removeClass('active');
        $(this).addClass('active');
      }
    });

    // client's device graph toggle
    $('.client-device li > span:first-child').on('click', function() {
      $(this).css('color', '#333');

      index = $(this).parent().index();

      if(hideDeviceGraph[index]) {
        hideDeviceGraph[index] = 0
        colors[index] = colorsCopy[index];
      } else {
        hideDeviceGraph[index] = 1;
        colorsCopy[index] = colors[index];
        colors[index] = '#333';
      }
    });

  });


  // show saved client's name
  socket.on('client_name', function(data) {
    for(key in data.data) {
      $('.client.' + key + ' .name span').html(data.data[key]);
      clientNames[key] = data.data[key];
    }
  });


  // processing client's pause
  socket.on('client_pause', function(data) {
    var pauseObject = JSON.parse(data.data.replace(/'/g, '"'));

    for(key in pauseObject) {
      if(key == 'pause') {
        $('.client.' + pauseObject.pause.replace(/\./g, '-')).addClass('pause');
        $('.client.' + pauseObject.pause.replace(/\./g, '-') + ' .pause-button i').removeClass('fa-pause').addClass('fa-play');
      } else {
        $('.client.' + pauseObject.work.replace(/\./g, '-')).removeClass('pause');
        $('.client.' + pauseObject.work.replace(/\./g, '-') + ' .pause-button i').removeClass('fa-play').addClass('fa-pause');
      }
    }
  });


  // processing client's disconnect
  socket.on('client_disconnect', function(data) {
    var disconnectObject  = JSON.parse(data.data.replace(/'/g, '"')),
    disconnectClassIP = disconnectObject.disconnect.replace(/\./g, '-');

    if($('.client.' + disconnectClassIP).hasClass('active')) {
      $('.client.' + disconnectClassIP).removeClass('active');
      $('ul.client-list > li:first-child').addClass('active');
    }

    $('.client.' + disconnectClassIP).addClass('animated fadeOutRight');
    if($('ul.client-list .client').length == 1) {
      $.plot('#graph', [ [0, 0] ], options);
    }

    setTimeout(function() {
      $('.client.' + disconnectClassIP).remove();
      if($('ul.client-list .client').length == 0) {
        $('.start-window').removeClass('fadeOutLeft').addClass('fadeInLeft');
      }
    }, 500);

  });


  // special scrollbar for client's list
  $('.client-list').scrollbar();

});