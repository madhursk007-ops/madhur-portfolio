const { app, BrowserWindow, Menu } = require('electron');
const path = require('node:path');
function createWindow() {
 const win = new BrowserWindow({width:1440,height:920,minWidth:980,minHeight:680,backgroundColor:'#f3f7f8',title:'MediBill Pharmacy Suite',webPreferences:{preload:path.join(__dirname,'preload.cjs'),contextIsolation:true,nodeIntegration:false,sandbox:true}});
 win.loadFile(path.join(__dirname,'index.html'));
 Menu.setApplicationMenu(null);
}
app.whenReady().then(()=>{createWindow();app.on('activate',()=>{if(BrowserWindow.getAllWindows().length===0)createWindow()})});
app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit()});
