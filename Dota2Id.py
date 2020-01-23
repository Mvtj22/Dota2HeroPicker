# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:45:49 2019

@author: velaz
"""
import json
import requests 
import Tkinter 
import numpy as np
import ttk 
from PIL import Image 
from PIL import ImageTk

#GLOBAL_VAR1 = 0
#GLOBAL_VAR2 = 0

'''Makes the main GUI window(includes name and size)'''
root= Tkinter.Tk()
root.title("Dota 2 Helper App")
root.geometry("1920x1080")

#gridFrame = ttk.Frame(root)

'''Change style for label'''
style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="white")
style.configure("default", padding=6, relief="flat", background="#ccc")

'''The base match url and number which is where we start finding matches'''
api_url_base = 'https://api.opendota.com/api/matches/5022879296'
api_match_id_number=5022879296

'''Reads in the Hero's name and Id from a Json File'''
f = open('heroesDump.txt', 'r')
heroes = json.loads(f.read())
f.close()

'''Makes a label on the root using text sent in'''
'''How to send in text: "Player Name: {0}".format(api_info['players'][x]['personaname']'''
def make_label(text):
    #global GLOBAL_VAR2
    #GLOBAL_VAR2 = GLOBAL_VAR2 +1 
    label=ttk.Label(root,text=text,style="BW.TLabel")
    #label.grid(row=0,column=GLOBAL_VAR2,pady=10,padx=10)
    #gridFrame.pack()
    label.pack()


'''Makes an image on the root just send in the path to the image and x and y values'''
def make_image(path,x2,y2):
    load = Image.open(path)
    render = ImageTk.PhotoImage(load)

    img = ttk.Label(root, image=render)
    img.image = render
    img.place(x=x2,y=y2)
    
'''Gets match information using the base url global variable, using the opendota api'''
'''Returns none if the api cannot get the match info'''
def get_api_info():
    
    #api_url = '{0}account'.format(api_url_base)
    
    response = requests.get(api_url_base, {'Content-Type': 'application/json'})
    print(api_url_base)
    print("Api Status Code: " , response.status_code)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_match_array():
    try:
     np.load('GameWinLose.npy')    
    except:
        games=np.zeros((129,129,2))
        np.save('GameWinLose', games)
        print("Made new NumpyArray")
    games=np.load('GameWinLose.npy')
    return games

def get_match_info():
    api_info = get_api_info()
    total_ranks_known = 0.0
    total_ranks_tensplace = 0.0
    total_ranks_onesplace = 0.0
    total_ranks_average = 0.0  
    y_total = 0.0

    
    if api_info is not None and api_info['lobby_type'] is 7:
        make_label("This is a ranked matchmaking game")
        for x in range(10):
            if(x is 0):
                make_label("")
                make_label("Radiant Team")
                make_label("")
            if (x is 5):
                make_label("")
                make_label("Dire Team")
                make_label("")
            if(api_info['players'][x]['account_id'] is not None):
                make_label("Player Name: {0}".format(api_info['players'][x]['personaname']))
                if api_info['players'][x]['rank_tier'] is  not None:
                    make_label("Ranked Medal: {0}".format(api_info['players'][x]['rank_tier']))
                    total_ranks_known = total_ranks_known + 1.0
                    total_ranks_tensplace = total_ranks_tensplace + (api_info['players'][x]['rank_tier'] - api_info['players'][x]['rank_tier'] % 10)/10
                    total_ranks_onesplace = total_ranks_onesplace + api_info['players'][x]['rank_tier'] % 10.0
                else:
                    make_label("Ranked Medal is uncalibrated")
            else:
                make_label("Player Name: Not Publicly Available")
            
            make_label("Hero Id: {0}".format(api_info['players'][x]['hero_id']))
            
            if x<5:
                for a in range(5):
                    games = get_match_array()
                    try:
                        make_label("Win Rate against {0} :".format(api_info['players'][5+a]['hero_id']) + str((games[(api_info['players'][x]['hero_id']-1),(api_info['players'][a+5]['hero_id']-1),0] / (games[(api_info['players'][x]['hero_id']-1),(api_info['players'][a+5]['hero_id']-1),1]))))
                    except:
                        make_label("Win Rate against {0} :".format(api_info['players'][5+a]['hero_id']) + str(0))
            if x>4:
                for b in range(5):
                    games = get_match_array()
                    make_label("Win Rate against {0} :".format(api_info['players'][a]['hero_id']) + str((games[(api_info['players'][x]['hero_id']-1),(api_info['players'][a]['hero_id']-1),0] / (games[(api_info['players'][x]['hero_id']-1),(api_info['players'][a]['hero_id']-1),1])))) 
            
    
            hero_1 = api_info['players'][x]['hero_id']
            
            if(api_info['radiant_win'] and x<5):
                games = get_match_array()
                for y in range(5):
                    games[(api_info['players'][x]['hero_id']-1),(api_info['players'][y+5]['hero_id']-1),0] +=1
                np.save('GameWinLose', games)
                
                for z in range(5):
                    games[(api_info['players'][z+5]['hero_id']-1),(api_info['players'][x]['hero_id']-1),1] +=1
                np.save('GameWinLose', games)
            elif (not(api_info['radiant_win']) and x>4):
                games = get_match_array()
                for y in range(5):
                    games[(api_info['players'][x]['hero_id']-1),(api_info['players'][y]['hero_id']-1),0] +=1
                np.save('GameWinLose', games)
                
                for z in range(5):
                    games[(api_info['players'][z]['hero_id']-1),(api_info['players'][x]['hero_id']-1),1] +=1
                np.save('GameWinLose', games)
            
            make_label(heroes[hero_1-1]['localized_name'])
            make_image("220px-{0}_icon.png".format(heroes[hero_1-1]['localized_name']),500,y_total)
            y_total = y_total +75
            make_label("")
    
        if(api_info['radiant_win']):
            make_label("Radiant has Won!")
        else:
            make_label("Dire has Won!")
        
        if total_ranks_known is not 0:
            total_ranks_average = (total_ranks_tensplace / total_ranks_known) * 10
            total_ranks_average = total_ranks_average + total_ranks_onesplace / total_ranks_known
            make_label("The average rank in this game was: {0}".format(int(total_ranks_average)))
        
                    
            
            
    #else:
    #    make_label('No relevent information!(aka it is None or it is not a ranked lobby)')
        
    
    
        
        
        



for x in range(100):
    api_match_id_number = api_match_id_number + 1
    api_match_id_number_string= str(api_match_id_number)
    api_url_base = api_url_base[0:37] + api_match_id_number_string
    get_match_info()
    api_info = get_api_info()
    if api_info is not None and api_info['lobby_type'] is 7:
        btn = ttk.Button(root,text="Quit",command=root.destroy)
        btn.pack()

        root.mainloop()
        root= Tkinter.Tk()
        root.title("Dota 2 Helper App")
        root.geometry("1920x1080")
    """np.set_printoptions(threshold=np.nan)
    print(get_match_array())"""
