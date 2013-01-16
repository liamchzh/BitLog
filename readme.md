#[关于BitLog](http://liamchzh.com/%E5%85%B3%E4%BA%8Ebitlog/)
BitLog是用python + tkinter写一款用于BIT的宽带认证客户端。

写这样一个软件的想法开始于2011年底，而真正开始是在2012年4月，从构思到编码再到debug完成花了一个多星期的全部课外时间。python是很强大的，做界面有wxpython和tkinter两种主流的方法，开始的时候比较了一下两者，最后决定使用tkinter进行开发。因为是一边学习一边开发，所以速度很慢，常常为了一个功能需要查大量的资料。
其实学校已经提供了官方的登陆客户端surn3000，相比于旧版本的surn3000，现在的版本不论从程序大小还是程序界面来说，都不如旧版本简洁，并且新版本的注销功能不太完善，所以才萌生自己写一个的想法。为了使软件尽量简洁，我只开发了最基本的功能——登陆和注销。

#[重写BitLog](http://liamchzh.com/%E9%87%8D%E5%86%99bitlog/)
花了点时间重新写了一下BitLog。

前一个版本是用tkinter写的，是我第一个用python写的有界面的小玩意。当时写的时候对tkinter了解甚少，基本是一边学习一边开发，所以最后代码结构非常凌乱，当时为了达到目的，胡乱地使用「类」。至于界面的美观性更不用谈了。
这个版本是用pygtk写的界面。也是一边学习一边开发，但是这次这个结构清晰多了，界面也更加简洁。

下面是界面截图：

![Alt text](http://liamchzh.com/wp-content/uploads/2013/01/BitLog%E4%B8%BB%E7%95%8C%E9%9D%A2.jpg)

![Alt text](http://liamchzh.com/wp-content/uploads/2013/01/BitLog%E8%AE%BE%E7%BD%AE.jpg)

![Alt text](http://liamchzh.com/wp-content/uploads/2013/01/BitLog%E5%85%B3%E4%BA%8E.jpg)
