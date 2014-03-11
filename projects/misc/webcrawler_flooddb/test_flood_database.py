""" Stress test GA flood database

This script tests that the flood database is live.
Then proceeds to crawl through the site based on a html file containing 1005 level 1 links. Detail links below are followed automatically.

If the database works, this test should complete with 3715 Detail links
responding succesfully


Ole Nielsen, RAMP 2006
x9048
"""



b_version = False

import urllib	
import string
#from caching import cache

if b_version is True:
    base_url = 'http://www-b.ga.gov.au/oracle/flood/'
    servlet_base_url = 'http://www-b.ga.gov.au/'
else:
    base_url = 'http://www.ga.gov.au:8500/oracle/flood/'
    servlet_base_url = 'http://www.ga.gov.au:8500/'    
    

def test_site():
    """Test flood database
    """
  
    top_url = 'flood_input.jsp'

    url = base_url+top_url
    live = False  
    print 'Testing %s. ' %url, 
    T = get_page(url)

    for line in T:
        #print line.strip()
        if line.startswith('<title>Geoscience Australia: Online Flood Search'):
            live = True
            break

    if live is True:    
        print 'OK: Page is live'
    else:
        msg = 'Page %s is not live' %url          
        raise msg

    print


def test_database(filename):
    """Read list of studies from html and try them one by one
    """

    print 'Reading %s' %filename
    fid = open(filename)

    total_detail = 0
    for i, link in enumerate(get_individual_studies(fid.readlines())):
        url = base_url+htmlmap(link)
      
        live = False  
        print 'Testing link %d: %s...' %(i, link[:72]),
        T = get_page(url)

        live = False 
        for line in T:
            if line.startswith('<tr><th>Dataset Name</th>') or\
                   line.startswith('<h2>Study title only available.</h2>'):
                live = True
                break
            
        if live is True:    
            print 'OK: Link %d is live' %i
        else:
            print 
            print 'HTML page that failed:', T
            #for line in T:
            #    print line.strip()
                
            msg = 'FAIL: Link %d is not live: %s' %(i,url)
            raise msg


        # Second tier links
        for j, link in enumerate(get_second_tier_links(T)):
            url = servlet_base_url+htmlmap(link)
      
            live = False  
            print 'Testing detail %d: %s...' %(j, link[:80]),
            T = get_page(url)

            live = False
            for line in T:
                if line.startswith('<tr><td><h3>Participants in '):
                  live = True
                  break

            if live is True:    
                print 'OK: Detail link %d is live (total=%d)' %(j, total_detail)
            else:
                print 
                print 'HTML page that failed:', T
                #for line in T:
                #    print line.strip()
                    
                msg = 'FAIL: Detail link %d is not live (total=%d)' %(j, total_detail)
                raise msg
                
            total_detail += 1            


def get_second_tier_links(lines):
    """Scan html lines for flood details and yield
    """   
    for line in lines:
      
        index = line.find('<a href="/servlet/FloodDetailServlet?sno')
        if index >= 0:
            start_index = line.find('servlet', index)
            end_index = line.find('">', start_index)
            yield line[start_index:end_index]

      

def get_individual_studies(lines):
    """Scan html lines for individual flood studies and yield links
    """ 
  
    for line in lines:
        index = line.find('<a href="%sflood_infolist.jsp?sno' %base_url)
        if index >= 0:
            start_index = line.find('flood_infolist', index)
            end_index = line.find('">', start_index)

            yield line[start_index:end_index]

      
def get_page(URL):
    """General routine for getting and caching URL pages
    """
  
    F = urllib.urlopen(URL)    
    T = F.readlines()
    return(T)



def htmlmap(s):
    import types
    from string import replace, strip

    s = replace(s,' ','%20')   
    return(strip(s))
	  

print 'Testing main site'
test_site()

print 'Reading html file'
if b_version is True:
    test_database('flood_studies_all_b.html')
else:
    test_database('flood_studies_all.html')
        
