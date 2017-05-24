$(document).ready(function() {
    //hover
    $('.btn-menu').on('mouseenter', function(){
        $(this).css('background-color', 'rgba(255,255,255,0.2)');
    });
    $('.btn-menu').on('mouseleave', function(){
        $(this).css('background-color', 'transparent');
    });

    $('body > .content').children().hide();
    //click
    $('#btn-company').on('tap', function(){
        $('.btn-menu').removeClass('pressed');
        $(this).addClass('pressed');

        $('body > .content').children().hide();
        $('#company-info').show();
        //get info
        $.postJSON(
            '/company-data',
            {},
            function(response) {
                $('#company-name').val(response.name);
                $('#company-sname').val(response.sname);
                $('#company-address').val(response.address);
                $('#company-welcome').val(response.welcome);
                $('#company-desc').val(response.desc);
            }
        );
    });
    $('#btn-diet').on('tap', function(){
        $('.btn-menu').removeClass('pressed');
        $(this).addClass('pressed');
        $('body > .content').children().hide();
        $('#diet-info').show();
    });
    $('#btn-desk').on('tap',function(){
        $('.btn-menu').removeClass('pressed');
        $(this).addClass('pressed');
        $('body > .content').children().hide();
        $('#desk-info').show();
    });
    $('#btn-faculty').on('tap', function(){
        $('.btn-menu').removeClass('pressed');
        $(this).addClass('pressed');
        $('body > .content').children().hide();
        $('#faculty-info').show();
    });

    $('#btn-history').on('tap',function(){
        $('.btn-menu').removeClass('pressed');
        $(this).addClass('pressed');
        $('body > .content').children().hide();
        $('#history').show();
    });
    $('#btn-cook').on('tap', function(){
        $('.btn-menu').removeClass('pressed');
        $(this).addClass('pressed');
        $('body > .content').children().hide();
        $('#cook-info').show();
    });


    //section company-info
    $('#company-submit').on('tap', function() {
        var name = $('#company-name').val();
        var sname = $('#company-sname').val();
        var address = $('#company-address').val();
        var welcome = $('#company-welcome').val();
        var desc = $('#company-desc').val();
        $.postJSON(
            '/company-info',
            {'name': json(name), 'sname': json(name), 'address': json(address), 'welcome': json(welcome), 'desc': json(desc)},
            function(response) {
                $('#company-name').val(response.name);
                $('#company-sname').val(response.sname);
                $('#company-address').val(response.address);
                $('#company-welcome').val(response.welcome);
                $('#company-desc').val(response.desc);
            }
        );
    });

    //section diet-info
    $('#btn-tab-cate').on('tap', function() {
        $('#diet-info .btn-tab').removeClass('pressed');
        $(this).addClass('pressed');

        $('#diet-info .cate').css('display', 'block');
        $('#diet-info .diet').css('display', 'none');
    });
    $('#btn-tab-diet').on('tap', function() {
        $('#diet-info .btn-tab').removeClass('pressed');
        $(this).addClass('pressed');
        $('#diet-info .cate').css('display', 'none');
        $('#diet-info .diet').css('display', 'block');
    });
    //diet-info cate
    $('#btn-cate-add-submit').on('tap', function(){
        var cid = trim($('#cid').val());
        var name = trim($('#c-name').val());
        var order = trim($('#c-order').val());
        var desc = trim($('#c-desc').val());
        if(cid == '' || name == '' || order == '') return;
        $.postJSON(
            '/cate-add',
            {'cid': json(cid), 'name':json(name), 'order': json(order), 'desc': json(desc)},
            function(res){
                showcate();
            }
        );
    });
    $('#btn-cate-del-submit').on('tap', function(){
        var cid = trim($('#cid2').val());
        if(cid == '') return;
        $.postJSON(
            '/cate-del',
            {'cid': json(cid)},
            function(res) {
                showcate();
            }
        );
    });

    $('#btn-cate-add').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.cate-add').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.cate-add').slideDown();
        }

    });
    $('#btn-cate-del').on('tap', function() {
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.cate-del').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.cate-del').slideDown();
        }
    });
    $('#btn-cate-show').on('tap', function(){
        showcate();
    });
    //diet-info diet
    $('#btn-diet-del-submit').on('tap', function(){
        var did = trim($('#did2').val());
        if(did == '') return;
        $.postJSON(
            '/diet-del',
            {'did': json(did)},
            function(response) {
                console.log(response);
            }
        );
    });

    $('#btn-diet-add').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.diet-add').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.diet-add').slideDown();
        }
    });

    $('#btn-diet-del').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.diet-del').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.diet-del').slideDown();
        }
    });
    $('#btn-diet-show').on('tap', function(){
        showdiet();
    });
    $('#diet-info').on('tap', '.pic', function(){
        //alert('tapped');
        $('.image-show').slideDown();
        var p = $(this).parents('tr');
        var d = p.data('data');
        var pic = d.picture;
        $('.image').attr('src', '/static/pictures/'+pic);
    });
    $('#diet-info').on('tap', '.image-close', function(){
        $('.image-show').slideUp();
    });

    //section desk-info
    $('#btn-desk-add-submit').on('tap', function(){
        var desk = trim($('#input-desk-add').val());
        if(desk == '') return;
        $.postJSON(
            '/desk-add',
            {'desk': json(desk)},
            function(res){
                showdesk();
            }
        );
    });
    $('#btn-desk-del-submit').on('tap', function(){
        var desk = trim($('#input-desk-del').val());
        if(desk == '') return;
        $.postJSON(
            '/desk-del',
            {'desk': json(desk)},
            function(res){
                showdesk();
            }
        );
    });
    $('#btn-desk-show').on('tap', function(){
        showdesk();
    });
    $('#btn-desk-add').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.desk-add').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.desk-add').slideDown();
        }
    });
    $('#btn-desk-del').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.desk-del').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.desk-del').slideDown();
        }
    });
    $('#btn-desk-download').on('tap', function(){
        $.postJSON(
            '/tar',
            {},
            function(){}
        );
    });

    //section faculty-info
    $('#btn-faculty-add-submit').on('tap', function(){
        var fid = trim($('#input-faculty-fid').val());
        var name = trim($('#input-faculty-name').val());
        var role = trim($('#input-faculty-role').val());
        var passwd = trim($('#input-faculty-passwd').val());
        if(fid == '' || name == '' || role == '' || passwd == '') return;
        $.postJSON(
            '/faculty-add',
            {'fid': json(fid), 'name': json(name), 'role': json(role), 'passwd': json(passwd)},
            function (response) {
                showfaculty();
            }
        );
    });
    $('#btn-faculty-del-submit').on('tap', function(){
        var fid = trim($('#input-faculty-fid2').val());
        if(fid == '') return;
        $.postJSON(
            '/faculty-del',
            {'fid': json(fid)},
            function(response) {
                showfaculty();
            }
        );
    });
    $('#btn-faculty-show').on('tap', function(){
        showfaculty();
    });
    $('#btn-faculty-add').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.faculty-add').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.faculty-add').slideDown();
        }
    });
    $('#btn-faculty-del').on('tap', function(){
        if($(this).hasClass('pressed')) {
            $(this).removeClass('pressed');
            $('.faculty-del').slideUp();
        } else {
            $(this).addClass('pressed');
            $('.faculty-del').slideDown();
        }
    });

    //section history
    $('#btn-tab-period').on('tap', function(){
        $('#history .btn-tab').removeClass('pressed');
        $('#history .tab-content').children().hide();
        $(this).addClass('pressed');
        $('#history .period').show();

    });
    $('#btn-tab-trend').on('tap', function(){
        $('#history .btn-tab').removeClass('pressed');
        $('#history .tab-content').children().hide();
        $(this).addClass('pressed');
        $('#history .trend').show();
    });

    $('#btn-period-submit').on('tap',function(){
        var from = trim($('#input-timefrom').val());
        var to = trim($('#input-timeto').val());
        if(from == '' || to == '') return;
        $.postJSON(
            '/period',
            {'from': json(from), 'to': json(to)},
            function(response) {
                if(response.status != 'ok') return;
                showperiod(response);
            }
        );
    });

    // trend
    $('#btn-trend-submit').on('tap', function(){
        var num = trim($('#input-trend-num').val());
        var base = trim($('#input-trend-base').val());
        if(num == '' || num == 0) return;
        $.postJSON(
            '/trend',
            {'num': json(num), 'base': json(base)},
            function(response){
                if(response.status != 'ok') return;
                showtrend(response);
            }
        );
    });
    //section cook-info
    $('#btn-cook-submit').on('tap', function(){
        var from = trim($('#input-cook-from').val());
        var to = trim($('#input-cook-to').val());
        if(from == '' || to == '') return;
        $('.cook-work').remove();
        window.tapped = [];
        window.from = from;
        window.to = to;
        $.postJSON(
            '/cook-info',
            {'from': json(from), 'to': json(to)},
            function(response) {
                console.log(response);
                if(response.status != 'ok') return;
                showcook(response);
            }
        );
    });
    $('#all-work-table').on('tap', '.detail', function(){
        //alert('tapped');
        var item = $(this).parents('tr').data('data');
        var fid = item.fid;
        var name = item.name;
        if($(this).hasClass('pressed')) {
            //hide
            $(this).removeClass('pressed');
            $('.cook-work').each(function(){
                if($(this).data('fid') == fid) $(this).hide();
            });
        } else {
            //show
            $(this).addClass('pressed');
            showonecook(fid, name);
        }


    });

});

function showcate(){
    //clear
    $('#cate-table tbody').empty();

    //get cate data

    $.postJSON(
        '/cate-data',
        {},
        function(res) {
            console.log(res);
            data = res.cate;
            for(var i in data) {

                var item$ = $('<tr>'+
                                '<td><div class="cid">0001</div></td>'+
                                '<td><div class="name">主食</div></td>'+
                                '<td><div class="th">3</div></td>'+
                                '<td><div class="desc"></div></td>'+
                            '</tr>');
                item$.find('.cid').text(data[i].cid);
                item$.find('.name').text(data[i].name);
                item$.find('.th').text(data[i].ord)
                item$.find('.desc').text(data[i].description);
                $('#cate-table tbody').append(item$);
            }
        }
    );


}

function showdiet(){
    //clear
    var p = $('#diet-table tbody').empty();
    //get data
    $.postJSON(
        '/diet-data',
        {},
        function(response) {
            var data = response.diet;
            for(var i in data) {
                var item$ = $('<tr>'+
									'<td><div class="did">0001</div></td>'+
									'<td><div class="name">主食</div></td>'+
									'<td><div class="th">3</div></td>'+
									'<td><div class="price">26.0</div></td>'+
									'<td><div class="base">1</div></td>'+
									'<td><div class="cid">3</div></td>'+
									'<td><a href="javascript:void(0)" class="pic">查看</a></td>'+
									'<td><div class="desc">无fdffgdgf</div></td>'+
								'</tr>');
                item$.find('.did').text(data[i].did);
                item$.find('.name').text(data[i].name);
                item$.find('.th').text(data[i].ord);
                item$.find('.price').text(data[i].price);
                item$.find('.base').text(data[i].base);
                item$.find('.cid').text(data[i].cid);

                item$.find('.desc').text(data[i].description);
                item$.data('data', data[i]);
                p.append(item$);
            }
        }
    );
    //show
}

function showdesk(){
    //clear
    var p = $('#desk-info .desk-view .container').empty();
    $.postJSON(
        '/desk-data',
        {},
        function(response){
            console.log(response);
            var data = response.desks;
            for (var i in data) {
                var item$ = $('<div class="desk">1</div>');
                item$.text(data[i]);
                p.append(item$);
            }
        }
    );
}

function showfaculty(){
    //clear
    var p = $('#faculty-table tbody').empty();

    $.postJSON(
        '/faculty-data',
        {},
        function(response) {
            if(response.status != 'ok') return;
            var data = response.faculty;
            for(var i in data) {
                var item$ = $('<tr>'+
									'<td><div class="fid">0001</div></td>'+
									'<td><div class="name">Jack</div></td>'+
									'<td><div class="role">3</div></td>'+
									'<td><div class="passwd">无</div></td>'+
								'</tr>');
                item$.find('.fid').text(data[i].fid);
                item$.find('.name').text(data[i].name);
                item$.find('.role').text(data[i].role);
                item$.find('.passwd').text(data[i].password);
                p.append(item$);
            }
        }
    );
}

function showperiod(data) {
    var order = data.order;
    var feedback = data.feedback;

    //clear
    var p1 = $('#sum-table tbody').empty();
    var p2 = $('#feedback-table tbody').empty();

    for(var i in order) {
        var item1 = $('<tr>'+
                            '<td class="did">0001</td>'+
                            '<td class="name">宫保鸡丁</td>'+
                            '<td class="num">1</td>'+
                            '<td class="price">1</td>'+
                            '<td class="total-price">0</td>'+
                            '<td class="percentage">0</td>'+

                        '</tr>');
        item1.find('.did').text(order[i].did);
        item1.find('.name').text(order[i].name);
        item1.find('.num').text(order[i].num);
        item1.find('.price').text(order[i].price);
        item1.find('.total-price').text(order[i].total);
        item1.find('.percentage').text(order[i].percentage);
        p1.append(item1);
    }

    for(var j in feedback) {
        var item2 = $('<tr>'+
                            '<td class="did">0001</td>'+
                            '<td class="name">宫保鸡丁</td>'+
                            '<td class="num">1</td>'+
                            '<td class="good">1</td>'+
                            '<td class="normal">0</td>'+
                            '<td class="bad">0</td>'+

                        '</tr>');
        item2.find('.did').text(feedback[j].did);
        item2.find('.name').text(feedback[j].name);
        item2.find('.num').text(feedback[j].num);
        item2.find('.good').text(feedback[j].good);
        item2.find('.normal').text(feedback[j].normal);
        item2.find('.bad').text(feedback[j].bad);
        p2.append(item2);
    }



}

function showtrend(data){
    var trend = data.trend;
    labels = trend[0];
    dat = trend[1];
    var d = {
            labels : labels,
            datasets : [

                {
                    fillColor : "rgba(151,187,205,0.5)",
                    strokeColor : "rgba(151,187,205,1)",
                    pointColor : "rgba(151,187,205,1)",
                    pointStrokeColor : "#fff",
                    data : dat
                }
                    ]
            };
    var ctx = document.getElementById("map").getContext("2d");
    var myNewChart = new Chart(ctx).Line(d,{responsive: true});


}

function showcook(data) {
    d = data.cook;
    //(cook, num, total)
    cook = d[0];
    //clear
    var p = $('#all-work-table tbody').empty();

    for(var i in cook) {
        var item = $('<tr>'+
                        '<td class="fid">0004</td>'+
                        '<td class="name">厨师</td>'+
                        '<td class="num">1</td>'+
                        '<td class="num_per">100</td>'+
                        '<td class="total">26.0</td>'+
                        '<td class="total_per">100</td>'+
                        '<td><a class="detail" href="javascript:void(0)">查看</a></td>'+

                    '</tr>');
        item.data('data', cook[i]);
        item.find('.fid').text(cook[i].fid);
        item.find('.name').text(cook[i].name);
        item.find('.num').text(cook[i].num);
        item.find('.num_per').text(cook[i].num_per);
        item.find('.total').text(cook[i].total);
        item.find('.total_per').text(cook[i].total_per);
        p.append(item);
    }
    var last = $('<tr>'+
                    '<td class="fid"></td>'+
                    '<td class="name"></td>'+
                    '<td class="num"></td>'+
                    '<td class="num_per"></td>'+
                    '<td class="total"></td>'+
                    '<td class="total_per"></td>'+
                    '<td></td>'+

                '</tr>');
    last.find('.num').text(d[1]);
    last.find('.total').text(d[2]);
    p.append(last);

}

function showonecook(fid, name) {
    var flag = false;
    for(var i in window.tapped) {
        if(tapped[i] == fid) {
            flag = true;
            break;
        }
    }
    if(flag) {
        //tapped already just show
        $('.cook-work').each(function(){
            if($(this).data('fid') == fid) {
                $(this).show();
            }
        });
    } else {
        window.tapped.push(fid);
        //generate instantly
        var div$ = $('<div class="cook-work">'+
					'<div class="heading"></div>'+
					'<div class="fid"></div>'+
					'<table>'+
						'<thead>'+
							'<tr>'+
								'<th>编号</th>'+
								'<th>名称</th>'+
								'<th>数量</th>'+
								'<th>好吃</th>'+
								'<th>一般</th>'+
								'<th>不好吃</th>'+
							'</tr>'+
						'</thead>'+
						'<tbody>'+

						'</tbody>'+
					'</table>'+
				'</div>');
        div$.data('fid', fid);
        div$.find('.heading').text(name);
        div$.find('.fid').text(fid);
        $('.all-work').after(div$);

        $.postJSON(
                '/one-cook-info',
                {'fid': json(fid), 'from': json(window.from), 'to': json(window.to)},
                function(response) {
                    if(response.status != 'ok') return;
                    data = response.onecook;
                    for(var i in data) {
                        var tr$ = $('<tr>'+
                                        '<td class="did">0001</td>'+
                                        '<td class="name">宫保鸡丁</td>'+
                                        '<td class="num">1</td>'+
                                        '<td class="good">1</td>'+
                                        '<td class="normal">0</td>'+
                                        '<td class="bad">0</td>'+
                                    '</tr>');
                        tr$.find('.did').text(data[i].did);
                        tr$.find('.name').text(data[i].name);
                        tr$.find('.num').text(data[i].num);
                        tr$.find('.good').text(data[i].good);
                        tr$.find('.normal').text(data[i].normal);
                        tr$.find('.bad').text(data[i].bad);
                        div$.find('tbody').append(tr$);

                    }

                }
            );
    }



}
