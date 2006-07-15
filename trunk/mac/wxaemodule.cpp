#include <Python.h>  
#include <wx/wxPython/wxPython.h> 
 
 
#include <stdio.h>  
#ifdef __cplusplus  
extern "C" {  
#endif  
#include <Carbon/Carbon.h>  
#ifdef __cplusplus  
}  
#endif  
  
#define  kURLEventClass  'GURL'  
#define  kGetURLEvent    'GURL'  
  
static PyObject *my_callback = NULL;  
  
static OSErr MyHandleGURL(AppleEvent *theAppleEvent, 
                          AppleEvent* reply, 
                          long handlerRefCon)  
{  
  OSErr   err;  
  DescType  returnedType;  
  Size    actualSize;  
  char    URLString[255];   
  
  if ((err = AEGetParamPtr(theAppleEvent, keyDirectObject, typeChar, &returnedType,   
			   URLString, sizeof(URLString)-1, &actualSize)) != noErr){  
    return err;  
  }  
  
  URLString[actualSize] = 0;    // Terminate the C string  
  
  if (my_callback){  
    PyObject *arglist, *result;  
    arglist = Py_BuildValue("(s)", URLString);  
    wxPyBlock_t blocked = wxPyBeginBlockThreads();  
    result = PyEval_CallObject(my_callback, arglist);  
    if (result){  
      Py_DECREF(arglist);  
    }  
    wxPyEndBlockThreads(blocked);  
  }  
  
  return noErr;  
}  
  
static PyObject * setgurlhandler(PyObject *dummy, PyObject *args) 
{  
  OSErr err;  
  PyObject *result = NULL;  
  PyObject *temp;  
  AEEventHandlerUPP upp;  
  
  if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {  
    if (!PyCallable_Check(temp)) {  
      PyErr_SetString(PyExc_TypeError, "parameter must be callable");  
      return NULL;  
    }  
    Py_XINCREF(temp);         /* Add a reference to new callback */  
    Py_XDECREF(my_callback);  /* Dispose of previous callback */  
    my_callback = temp;       /* Remember new callback */  
    /* Boilerplate to return "None" */  
    Py_INCREF(Py_None);  
    result = Py_None;  
    upp = NewAEEventHandlerUPP((AEEventHandlerProcPtr)MyHandleGURL);  
    err = AEInstallEventHandler('GURL', 'GURL', upp, 0, FALSE);  
  }  
  return result;  
}  
  
static PyMethodDef wxAEMethods[] = {  
  {"setgurlhandler", setgurlhandler, METH_VARARGS, "setgurlhandler(func)"},  
  {NULL, NULL, 0, NULL}  
};    
      
#ifdef __cplusplus  
extern "C" {  
#endif  
  void initwxae(void){  
    wxPyCoreAPI_IMPORT();  
    (void)Py_InitModule("wxae", wxAEMethods);  
  }   
#ifdef __cplusplus  
}  
#endif   
