from gui import TomographView
import wx


def main():
    app = wx.App()
    TomographView(None)
    app.MainLoop()


if __name__ == '__main__':
    main()
