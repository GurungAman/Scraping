function login(){
    var username = $("#username").val();
    var password = $("#password").val();
    console.log(username)
    console.log(password)
    if(username!="" && password!=""){
        $.ajax({
            url: "http://127.0.0.1:8000/get_token/",
            type: "POST",
            data:{
                'username': username,
                'password': password,
            },
            success:function(data){
                document.cookie="token="+data['token'];
                console.log(data)
                window.location.href = "/scrape/";
            },
            error:function(data){
                console.log(data)
            }
        });
    }
};

function verify(){
    tokens = (document.cookie).toString().split(";");
    var token;
    tokens.forEach(ele => {
        if (ele.includes("token")){
            token = ele.split('=')[1]
        } 
    })
    $.ajax({
        url : "http://127.0.0.1:8000/verify_token/", 
        type : "GET",
        headers : {
            "Authentication": "JWT " + token
        },
        success:function(data){
            console.log("Success")
            console.log(data['status'])
            if (data['status'] == false){
                window.location.href = "http://127.0.0.1:8000/";
            }
        },
        error:function(data){
            window.location.href = "http://127.0.0.1:8000/";
            console.log(data)
        }
    });
};


function check_url(){
    var link = $('#url').val()
    var single_page = $('#single_page').is(':checked')
    var whole_site = $('#whole_page').is(':checked')
    var get_images = $('#get_images').is(':checked')
    var get_js = $('#get_js').is(':checked')
    var get_css = $('#get_css').is(':checked')
    var internal_links = $('#internal_links').is(':checked')
    $.ajax({
        url: "/check_url/",
        type: "POST",
        data: JSON.stringify({
            'url' : link,
            'single_page': single_page,
            'whole_site': whole_site,
            'get_images': get_images,
            'get_js': get_js,
            'get_css': get_css,
            'get_links': internal_links
        }),
        success:function(data){
            if (data['status'] == true){
                window.location.href = "http://127.0.0.1:8000/completed/"
            }
            else {
                alert("Invalid URL.")
            }
        },
        error:function(data){
            console.log(data)
            console.log("vayena")
        },
    });
};
