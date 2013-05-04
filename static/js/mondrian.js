function random_select(arr) {
    index = Math.floor(Math.random() * arr.length);
    return arr[index];
}

function sample_exp(lambda) {
    r = Math.random();
    return -1.0 * Math.log(1 - r) / lambda
}

var Mondrian = function(container, budget, images) {

  this.container = container;
  this.container_scale = container.offsetHeight;
  this.images = images;
  this.budget = budget;
  this.draw_mondrian_inner(this.container, budget, images);
}

Mondrian.prototype.p_replace = 0.3;
Mondrian.prototype.p_split = 0.65;

Mondrian.prototype.draw_mondrian_inner = function(par, budget, imgs) {
  var width = par.offsetWidth;
  var height = par.offsetHeight;
  par.setAttribute('mondrian-budget', budget);
  var cost = sample_exp((width + height) / 1080);

  if(cost < budget) {
    var remaining = budget - cost;
    var cut_frac = (0.5*Math.random() + 0.25)
    var cut = cut_frac * (width + height);
    var child1 = document.createElement('div'),
        child2 = document.createElement('div');

    if(cut < width) {

      child1.setAttribute('class', 'mondrian-horiz-block-1 mondrian-block');
      child1.setAttribute('style', 'width: ' + cut / width * 100  + '%;')

      child2.setAttribute('class', 'mondrian-horiz-block-2 mondrian-block');
      child2.setAttribute('style', 'width: ' + (1 - cut / width) * 100 + '%;')

    } else {
      var height_frac = (cut - width) / height;

      child1.setAttribute('class', 'mondrian-vert-block-1 mondrian-block');
      child1.setAttribute('style', 'height: ' + height_frac * 100  + '%;')

      child2.setAttribute('class', 'mondrian-vert-block-2 mondrian-block');
      child2.setAttribute('style', 'height: ' + (1 - height_frac) * 100 + '%;')
    }

    par.appendChild(child1);
    par.appendChild(child2);

    this.draw_mondrian_inner(child1, remaining, imgs);
    this.draw_mondrian_inner(child2, remaining, imgs);


  } else {
    var imgNode = document.createElement('img');
    imgNode.className = 'mondrian-tile';
    imgNode.setAttribute('src', random_select(this.images));
    par.appendChild(imgNode);
  }
}

Mondrian.prototype.add_image = function(src) {
  var tiles = document.querySelectorAll('.mondrian-tile');
  var targ = random_select(tiles);
  var par = targ.parentElement;

  var width = par.offsetWidth;
  var height = par.offsetHeight;
  var cost = sample_exp((width + height) / this.container_scale);
  var budget = par.getAttribute('mondrian-budget');

  if(cost < budget) {
    var remaining = budget - cost;
    var cut_frac = (0.5*Math.random() + 0.25)
    var cut = cut_frac * (width + height) ;
    var child1 = document.createElement('div'),
        child2 = document.createElement('div');

    if(cut < width) {
      child1.setAttribute('class', 'mondrian-horiz-block-1 mondrian-block');
      child1.setAttribute('style', 'width: ' + cut / width * 100  + '%;')

      child2.setAttribute('class', 'mondrian-horiz-block-2 mondrian-block');
      child2.setAttribute('style', 'width: ' + (1 - cut / width) * 100 + '%;')

    } else {
      var height_frac = (cut - width) / height;
      child1.setAttribute('class', 'mondrian-vert-block-1 mondrian-block');
      child1.setAttribute('style', 'height: ' + height_frac * 100  + '%;')

      child2.setAttribute('class', 'mondrian-vert-block-2 mondrian-block');
      child2.setAttribute('style', 'height: ' + (1 - height_frac) * 100 + '%;')
    }

    child1.appendChild(targ);
    var imgNode = document.createElement('img');
    imgNode.className = 'mondrian-tile';
    imgNode.setAttribute('src', src);
    child2.appendChild(imgNode);

    var newPar = document.createElement('div');
    newPar.className = par.className;
    var grandPar = par.parentElement;
    grandPar.replaceChild(par, newPar);

  } else {
    targ.setAttribute('src', src);
  }
}


