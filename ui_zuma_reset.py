import maya.cmds as cmds
import time
import datetime
from collections import OrderedDict

#############################################################
#########  FEATURE: RESET STATE #############################
#############################################################
def reset_attribs(obj):
    #attributi base
    defaultAttrs =  cmds.listAttr(obj, keyable=True)
    if defaultAttrs == None: return
    for eachAttr in defaultAttrs:
        if (eachAttr.startswith("translate") or
            eachAttr.startswith("rotate") ):
            cmds.setAttr(obj+"."+eachAttr, 0)
        elif eachAttr.startswith("scale"):
            cmds.setAttr(obj+"."+eachAttr, 1)
            
    #attributi user defined
    userAttrs = cmds.listAttr(obj, keyable=True, userDefined=True)
    if userAttrs == None: return
    for eachAttr in userAttrs:
        pointer = obj+"."+eachAttr
        defaultValue = cmds.addAttr(pointer, query=True,defaultValue=True)
        cmds.setAttr(pointer, defaultValue)

def reset_controls():    
    ctrls = cmds.ls(['*_ac_*','*_fk_*'], type='nurbsCurve' )
    
    for each_ctrl in ctrls:
       ctrl_parent = cmds.listRelatives(each_ctrl, parent=True)[0]
       reset_attribs(ctrl_parent)          

    CONTROL_STATES = OrderedDict()



#############################################################
#########  FEATURE: SAVE STATE ##############################
#############################################################
def save_attribs(obj, state):
    #attributi base
    defaultAttrs =  cmds.listAttr(obj, keyable=True)
    if defaultAttrs == None: return
    for eachAttr in defaultAttrs:
        if (eachAttr.startswith("translate") or
            eachAttr.startswith("rotate") or
            eachAttr.startswith("scale") ):
                key = obj+"."+eachAttr
                val = cmds.getAttr(key)
                state[key] = val
    #attributi user defined
    userAttrs = cmds.listAttr(obj, keyable=True, userDefined=True)
    if userAttrs == None: return
    for eachAttr in userAttrs:
        key = obj+"."+eachAttr
        val = cmds.getAttr(key)
        state[key] = val

CONTROL_STATES = OrderedDict()
def save_controls(label):    
    ctrls = cmds.ls(['*_ac_*','*_fk_*'], type='nurbsCurve' )
    
    state = {}
    for each_ctrl in ctrls:
       ctrl_parent = cmds.listRelatives(each_ctrl, parent=True)[0]
       save_attribs(ctrl_parent, state)          
    CONTROL_STATES[label] = state
    
#############################################################
#########  FEATURE: LOAD STATE ##############################
#############################################################
def load_controls(aState):    
    selectedState = CONTROL_STATES[aState];
    
    for key in selectedState.iterkeys():
        val = selectedState[key]
        cmds.setAttr(key, val)
        
        

#############################################################
#########  FEATURE: UI      #################################
#############################################################
def main():    
    cmds.window(title='Zoma Controls')
    
    cmds.columnLayout()
    cmds.button(label='Reset State', command=reset_listener)
    cmds.button(label='Save State',  command=save_listener)    
    cmds.setParent('..')
    
    cmds.rowLayout(numberOfColumns=2)
    cmds.optionMenu('state_list', label='Load State', changeCommand=load_listener)
    for each in CONTROL_STATES.iterkeys():
        cmds.menuItem( label=each)
    #cmds.button(label='Load',  command=load_listener)
    cmds.setParent('..')
    
    cmds.showWindow()
    
def save_listener(*args):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    save_controls(st)
    cmds.menuItem(label=st, parent='state_list')
    
def load_listener(*args):
    selected = cmds.optionMenu('state_list', query=True, value=True)
    load_controls(selected)

def reset_listener(*args):
    menuItems = cmds.optionMenu('state_list', query=True, itemListLong=True)
    if menuItems:
        cmds.deleteUI(menuItems)           
    reset_controls()

#############################################################
#########  TESTING    #######################################
#############################################################
def clean(): 
    cmds.select(all=True)
    cmds.delete()

def scenario01():
    cmds.file('C:\\_fdf\\projects\\workspace_aiv\\lessons\\LEZ47_20180424_MAYA_3_MEL\\model__zoma_hi_base_vanilla_rig_v6.ma',open=True, newFile=False, force=True)
        
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    save_controls(st);
    
    cmds.setAttr("zoma_ac_lf_footik.rotateY", 45)
    ts+=1
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    save_controls(st);
    
    cmds.setAttr("zoma_fk_rt_shoulder.rotateY", 45)
    ts+=1
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    save_controls(st);


CONTROL_STATES=OrderedDict()    
scenario01()

main()

clean()
