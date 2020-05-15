package com.github.izgzhen.wala.demo;

import com.ibm.wala.cast.js.ipa.callgraph.JSCallGraphUtil;
import com.ibm.wala.cast.js.translator.CAstRhinoTranslatorFactory;
import com.ibm.wala.cast.js.util.JSCallGraphBuilderUtil;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.util.CancelException;
import com.ibm.wala.util.WalaException;

import java.io.IOException;
import java.nio.file.Paths;
import java.nio.file.Path;

/* Created at 5/15/20 by zhen */
public class Main {
    public static void main(String[] args) throws CancelException, IOException, WalaException {
        Path path = Paths.get(args[0]);
        JSCallGraphUtil.setTranslatorFactory(new CAstRhinoTranslatorFactory());
        CallGraph cg = JSCallGraphBuilderUtil.makeScriptCG(path.getParent().toString(), path.getFileName().toString());
        System.out.println(cg.getNumberOfNodes());
    }
}
