
from Resource import PathResource as path
import pygsheets



def normalize(name):
    if name is not None:
        return name.strip().lower().replace(' ','')
    else:
        return


class get_allocate:
    def __init__(self, token, sheetname):
        self.allocated = {}
        self.token = token
        self.sheetname = sheetname
        self.make_object()

    def read_googlesheet(self):
        gc = pygsheets.authorize(service_file=path.resource_path(self.token))
        sh = gc.open(self.sheetname)
        wks =sh.worksheet('title','OverallcourseCompletion')
        read = wks.get_all_values()
        return read

    def make_object(self):

        for r in self.read_googlesheet()[1:]:
            print(r[11])
            if '-' in r[10]:
                course_title = r[10].split('-',1)[1]
                groups = eval(f"""r[10].split('-',1)[0]{".split(',')" if ',' in r[10].split('-')[0] else ''}""")
                if type(groups) != list:
                    groups = [groups]
                for g in groups:
                    g = normalize(g)
                    course_title = normalize(course_title)
                    if g not in self.allocated.keys() and course_title != '' and int(r[11]) == 1:
                        self.allocated[g] = [course_title]
                    elif course_title != '' and int(r[11]) == 1:
                        self.allocated[g].append(course_title)
        return self.allocated

    def check_allocate(self, title, group):
        if normalize(group) in self.allocated.keys() and normalize(title) in self.allocated[normalize(group)]:
            return 1
        else:
            return 0

