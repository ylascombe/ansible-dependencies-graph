#! /usr/bin/python3
"""
Browse an ansible roles directory and build dependency graph between roles
"""
import sys
import argparse
import yaml
from os.path import join
from glob import glob
import graphviz
from graphviz import Digraph

class Helper:

    def parse_args(self, argv):
        """
        Main function. Parse args and launch command.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--roles_path",
                            help="Path to ansible roles directory",
                            default="roles",
                            metavar='ROLES_DIR',
                           type=str)
        parser.add_argument("-o", "--output",
                            help="Output dependency graph filename",
                            default="roles-dependencies.png",
                            type=str)
        return parser.parse_args(argv)

class DependencyGraphHelper:

    def __init__(self):
        self._roles = {}
        self.graph = Digraph(comment='roles', node_attr={'color': 'lightblue2', 'style': 'filled'})
        
    def parse_roles(self, roles_dir):
        print("parsing roles_dir:" + roles_dir)

        self._search_in_metas(roles_dir)
        self._search_in_tasks(roles_dir, 'include_role')
        self._search_in_tasks(roles_dir, 'import_role')

        return self.graph

    def render_graph(self, graph, output_file):
        graph.attr(size='6,6')
        graph.render(output_file, view=True)

    def _search_in_metas(self, roles_dir):
        for path in glob(join(roles_dir, '*/meta/main.yml')):
            print("parsing path:" + path)
            dependent_role = path.split('/')[-3]

            with open(path, 'r') as f:
                self._search_in_meta(dependent_role, f.read())

    def _search_in_meta(self, dependent_role, file_content):
        for dependency in yaml.load(file_content, Loader=yaml.FullLoader)['dependencies']:
            depended_role = dependency['role']

            self._add_role_dependency(dependent_role, depended_role)

    def _search_in_tasks(self, roles_dir, searched_item):
        for task_file in glob(join(roles_dir, '*/tasks/*.yml')):
            dependent_role = task_file.split('/')[-3]

            with open(task_file, 'r') as f:
                file_content = f.read()
                self._search_item(dependent_role, file_content, searched_item)
                
    
    def _search_item(self, dependent_role, file_content, searched_item):
        if searched_item in file_content:
    
            try:
                for task in yaml.load(file_content, Loader=yaml.SafeLoader):
                    for key, value in task.items():
                        if searched_item == key:
                            depended_role = value['name']
                            print("searched_item on " + dependent_role + "-> " + depended_role)
                            self._add_role_dependency(dependent_role, depended_role)
            except yaml.parser.ParserError:
                print("Error")

    def _add_role(self, role):
        if role not in self._roles:
            self._roles[role] = self.graph.node(role, role)

    def _add_role_dependency(self, dependent_role, depended_role):
        #print("dependent_role " + dependent_role + " depended_role " + depended_role)
        self._add_role(depended_role)
        self._add_role(dependent_role)
        self.graph.edge(
            dependent_role,
            depended_role
        )

def main():
    helper = Helper()
    config = helper.parse_args(sys.argv[1:])

    graph_builder = DependencyGraphHelper()
    graph = graph_builder.parse_roles(config.roles_path)
    graph_builder.render_graph(graph, config.output)

if __name__ == '__main__':
    main()
