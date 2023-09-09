//abbr plugins dialog 
CKEDITOR.dialog.add('carouselDialog', function (editor) {
    return {
        title: 'carousel setting',
        minWidth: 400,
        minHeight: 200,

        contents: [{
            id: 'tab-basic',
            label: 'Basic Settings',
            elements: [{
                type: "html",
                id: "list",
                html: '<div id="picsList">' +
                    '<style>#picsList{font-style:14px}#picsList #addbtn{min-width:60px;padding:2px 5px;height:30px;font-size:14px;text-align:center;border:1px solid #ccc;margin-bottom:10px}#picsList>div{margin-bottom:5px}#picsList>div label{font-size:16px;margin-right:5px}#picsList>div input[type=text]{border:1px solid #ccc;height:24px;line-height:24px;width:300px}#picsList>div input[type=number]{border:1px solid #ccc;height:24px;line-height:24px;width:80px}</style>' +
                    '<button id="addbtn">Add Picture</button>' +
                    '<div><label for="width_set">Width</label><input id="width_set" type="number" />px，<label for="height_set">Height</label><input id="height_set" type="number" />px,<label for="delay_time">DelayTime</label><input id="delay_time" type="number" />s</div>' +
                    '<div><label for="pic_1">pic_1</label><input id="pic_1" type="text" /></div>' +
                    '<div><label for="pic_2">pic_2</label><input id="pic_2" type="text" /></div>' +
                    '</div>',
            }]
        }],
        onShow: function () {
            //console.log(this.getElement().getFirst());
            $("addbtn").addEventListener('click', addItem, false);

            var dialog = this.getElement().getFirst();
            rootDialog = dialog;
            rootEl = rootDialog;
        },
        onOk: function () {
            var dialog = this;
            var carousel = editor.document.createElement('img');

            //填充carousel
            var carouselHtml = makeCarousel();

            editor.insertHtml(carouselHtml);
        }
    }
})

function $(id) {
    return document.getElementById(id);
}

function addItem() {
    var pEl = $("picsList"),
        len = $("picsList").childNodes.length - 2;

    //创建插入项目
    var oFrag = document.createDocumentFragment(),
        div = document.createElement('div'),
        label = document.createElement('label'),
        input = document.createElement('input');

    label.setAttribute('for', 'pic_' + len);
    var oText = document.createTextNode('pic_' + len);
    label.appendChild(oText);
    input.setAttribute('id', 'pic_' + len);
    input.setAttribute('type', 'text');

    div.appendChild(label);
    div.appendChild(input);

    oFrag.appendChild(div);

    pEl.appendChild(oFrag)
}

function makeCarousel() {
    var list = $('picsList').getElementsByTagName('input');
    var imgSrc = [],
        num_width = list[0].value,
        num_height = list[1].value,
        delay_time = list[2].value * 1000;

    for (var i = 3; i < list.length; i++) {
        if (list[i]) {
            imgSrc.push(list[i].value);
        }
    }

    var strHtml = "",
        guid = createGuid(5),
        scriptStr = '<script>var length = document.querySelector(".' + guid + '").children.length,i=0;setInterval(function(){var El = document.querySelector(".' + guid + '"),marginLeft = El.style.marginLeft,moveNum = marginLeft.split("").reverse().join;if(++i<length){El.style.marginLeft = "-"+i*' + num_width + '+"px";}else{El.style.marginLeft = "-0px";i=0;}},' + delay_time + ')</script>';
    console.log(scriptStr);


    for (var i = 0; i < imgSrc.length; i++) {
        var imgStr = '<img src="' + imgSrc[i] + '">';
        strHtml += imgStr;
    }
    var firstDiv = '<div class="carousel-container>';
    console.log(firstDiv);
    var br = '<br>' +
        console.log(br);
    var btn1Html = '<button id="prevBtn">Prev</button>';
    console.log(btn1Html);
    var btn2Html = '<button id="nextBtn">Next</button>';
    console.log(btn2Html);


    strHtml = '<div class="carousel-container">' +
        '<i class="fas fa-arrow-left" id="prevBtn"></i>' +
        '<i class="fas fa-arrow-right" id="nextBtn"></i>' +
        '<div class="carousel-slide">' +
        strHtml +
        '</div></div>';
    return strHtml;
}

console.log(strHtml);

//生成一个自定义长度的表示guid，由0-9，a-z组成
function createGuid(num) {
    var numberArr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        wordsArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
        guidStr = '',
        strSum = [];
    strSum = wordsArr.concat(numberArr);
    for (var i = 0; i < num; i++) {
        var s = strSum[Math.floor((Math.random() * strSum.length))];
        if (typeof s == "number" && i == 0) {
            i--;
        } else {
            guidStr += s;
        }
    }

    return guidStr;
}