# -*- coding: utf-8 -*-

import yaml
import sys
import codecs

import markdown
from textwrap import dedent

import sys
if sys.version_info[0] >= 3:
    unicode = str

def write(html):
    print(html)

def functions_for_section(data, sec):
    funcs = data["functions"]
    return [f for f in funcs if f["group"] == sec]

def function_for_id(data, id):
    funcs = data["functions"]
    res = [f for f in funcs if f["id"] == id]
    if len(res) > 0:
        return res[0]
    return None

if __name__ == '__main__':
    source = codecs.open(sys.argv[1], mode='r', encoding='utf-8')    
    data = yaml.safe_load(source.read())
    total_examples = 0
    
    #Print header
    write("""
          <html>
            <head>
              <link rel="stylesheet" type="text/css" href="css/style.css">     
              <script src="lib/jquery-1.10.1.min.js" type="text/javascript" charset="utf-8"></script>                        
              <title>{name} &mdash; Codea</title>
              <script type="text/javascript" src="//use.typekit.net/zlz7now.js"></script>
              <script type="text/javascript">try{{Typekit.load();}}catch(e){{}}</script>    
            </head>
            <body>
              <a name="top"></a>
              <div class="documentation">
          """.format(**data))
          
    #Print title and subtitle
    write("""        
              <div class='header'>
                <img id='codea' src='images/Codea-Logo.jpg' height='200px'/>
                <div id='chapter'>
                    <div id='chapter-title'>
                    <h1>{name}</h1>
                    </div>
                </div>
              <h3 class="subtitle"><a href="index.html">Reference</a> ❯ {subtitle}</h3>
              </div>
          """.format(**data))
          
    #Print sections of document
    write("""
              <div class='outline'>
              <ul class="sec-ref">    
          """)
    sections = data["ordering"]          
    index = 1
    for s in sections:
        write("""
                <li><a href='#{index}'>{sec}</a></li>
              """.format(sec=s, index=index))
              
        funcs = functions_for_section(data, s)
      
        write(""" 
                <ul class="func-ref">             
            """)
        for f in funcs:
            write("""
                    <li class="type-tiny-icon type-{category}"><a href='#{id}'>{name}</a></li>
                  """.format(**f))                                 
        write(""" 
                </ul>             
              """)                      
              
        index = index+1
    write("""
              </ul>        
              </div>
          """)
    
    #Print the actual functions
    index = 1
    for s in sections:
        write("""
              <div class='section'>
              <h2><a name='{index}'>{sec}</a></h2>
              """.format(sec=s, index=index))
        
        funcs = functions_for_section(data, s)
        
        for f in funcs:
            write("""
                  <div class='function'>
                    <h3><div class='type-icon type-{category}'></div><a name='{id}'>{name}</a> <a class="toplink" href="#top">top ↑</a></h3>
                    <div class='function-body'>
                  """.format(**f))
                  
            #Print syntax                  
            if "syntax" in f:
                write("""      
                    <div class="syntax">  
                    <h4>Syntax</h4>          
                    <pre>{syntax}</pre>
                    </div>
                      """.format(**f))     
                      
            #Print description
            if "description" in f:
                uncdesc = unicode(f["description"])
                write("""                    
                    <div class='description'>
                      {description}
                    </div>
                      """.format(description=markdown.markdown(uncdesc)))                      
                      
            #Print out the function parameters
            if "parameters" in f:
                params = f["parameters"]
                write("""                  
                    <div class='parameters'>
                    <table>
                      """)                
                for p in params:
                    uncdesc = unicode(p["description"])
                    write("""  
                      <tr>
                        <td class="parameter-name">{name}</td>
                        <td class="parameter-desc">{description}</td>                
                      </tr>
                          """.format(name=p["name"], description=markdown.markdown(uncdesc)))                     
                
                write("""  
                    </table>                
                    </div>
                      """)
                      
            #Print out the examples
            if "examples" in f:                                                      
                exs = f["examples"]
                write("""                  
                    <div class='examples'>
                      <h4>Examples</h4>                    
                      """)
                for e in exs:
                    write("""  
                      <div id='example-{count}'>
{example}
                      </div>
                          """.format(example=e["example"],count=total_examples))                             
                    total_examples = total_examples+1
                write("""                  
                    </div>
                      """)   
                      
            #Print out return value
            if "returns" in f:
                write("""                  
                    <div class='returns'>
                      <h4>Returns</h4>
                      <p>{returns}</p>
                    </div>
                      """.format(returns=markdown.markdown(f["returns"])))                                                                  
            
            #Print related items
            if "related" in f:
                related = f["related"]
                write("""                  
                    <div class='related'>
                      <h4>Related</h4>                    
                      <ul>
                      """)
                for r in related:
                    rfunc = function_for_id(data, r)
                    if rfunc is not None:
                        write("""  
                      <li><a href='#{id}'>{name}</a></li>
                              """.format(name=rfunc["name"],id=r))                             
                write(""" 
                      </ul>                 
                    </div>
                      """)                

            write("""
                </div>
              </div>        
                  """)      
              
        write("""
              </div>        
              """)              
        index = index+1
          
    #Print end of document
    write("""
            </div>
            <script src="lib/ace.js" type="text/javascript" charset="utf-8"></script>    
            <script>            
                var editors = [];
          """)
    
    for i in range(0, total_examples):
        write("""            
                editors[{count}] = new ace.edit("example-{count}");
                editors[{count}].setReadOnly(true);
                editors[{count}].setHighlightActiveLine(false);
                editors[{count}].setShowInvisibles(false);                
                editors[{count}].setTheme("ace/theme/github");
                editors[{count}].getSession().setMode("ace/mode/lua");
                editors[{count}].resize()
              """.format(count=i))
    write("""           
                $(document).ready(function()
                {
                    for( var i = 0; i < editors.length; i++ )
                    {
                        var e = editors[i];
                        var height = e.getSession().getScreenLength() * e.renderer.lineHeight + e.renderer.scrollBar.getWidth();
                        
                        $('#example-'+i.toString()).height(height.toString()+'px');
                        
                        e.resize();
                    }    
                });
            </script>
            </body>
          </html>
          """)
          
          
          
          
    
