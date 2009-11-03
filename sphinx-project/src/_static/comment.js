function loading(){
    $("body").prepend('<div id="loading">loading...</div>');
    $("div#loading").css("left", $(window).width()/2-30);
}

function unloading(){
    $("body div#loading").remove();
}

function load_comment(){
    loading();
    setTimeout(unloading, 5000);
    /*$j.ajax({
        url: "/pymotwcn/comment",
        data:{
            "action":"load",
            "page":$("div.bodywrapper div.body div.section:first").attr("id")
        },
        beforeSend: function(){
            loading();
        },
        complete: function(req, status){
            unloading();
            // show result
        }
    });*/
}
function show_error(obj, msg){
    var outer = obj.prev();
    if (!outer.children("span.error").length) {
        outer.append('<span class="error"></span>');
    }
    outer.children("span.error").html(msg);
}
function hide_error(obj){
    obj.prev().children("span.error").remove();
}
function click_send(){
    var outer = $(this).parents("div.commentbox");
    var text = outer.find("textarea.comment_text");
    var sender = outer.find("input.comment_name");
    if (text.val().length<2) show_error(text, "评论内容为空!"); else hide_error(text);
    if (sender.val().length<2) show_error(sender, "提交者为空!"); else hide_error(sender);
}
function show_commentbox(obj){
    var outer = obj.parent("div.comment").next();
    if(!outer.next("div.commentbox").length){
        outer.after('<div class="commentbox" style="display:none;"><p>现有评论:</p><dl><dt>aaa</dt><dd>xya</dd></dl><hr /><p>评论内容:</p><textarea class="comment_text" rows="4" style="width:100%"></textarea><p>提交者:</p><input class="comment_name" type="text"/><input class="comment_send" type="button" value="发送"/></div>');
        outer.next("div.commentbox").find("input.comment_send").bind("click", click_send);
    }
    outer.next("div.commentbox").slideDown();
    obj.children("div").css("background-position", "0 0");
    outer.css("background-color", "#FFFDC9");
}
function hide_commentbox(obj){
    var outer = obj.parent("div.comment").next();
    outer.next("div.commentbox").slideUp();
    obj.children("div").css("background-position", "-16px 0");
    outer.css("background-color", "white");
}
$(document).ready(function(){
    $("div.body > div.section").find("h1,ul,div.section h2,div.section p").each(function(){
        if (!$(this).prev("div.comment").length) {
            $(this).before('<div class="comment"><a class="comment_link" title="leave your comments"><div></div></a></div>');
        }
    });
    $("div.comment").css("left", $("div.document").offset().left+2);
    load_comment();
    $("a.comment_link").toggle(function(){
        show_commentbox($(this));
    }, function(){
        hide_commentbox($(this));
    });
});

