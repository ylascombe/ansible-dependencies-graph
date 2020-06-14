
import pytest
from graphviz import Digraph

from ansibledependenciesgraph.main import DependencyGraphHelper

SAMPLE_TASK_FILE = """
---

- name: Fail if example var is not defined.
  fail:
    msg: Please set example var
  when:
    (example is not defined or '' == example)

- name: Print debug var.
  debug:
    var: example

- name: Register foo and bar vars
  set_fact:
    foo: "foo{{ example }}"
    bar: "bar-{{ example }}"

- name: Call sample_include_role to make the job done.
  include_role:
    name: sample_include_role

- name: Retrieve azure facts.
  import_role:
    name: azure-facts

...
"""

SAMPLE_META_FILE = """
---
dependencies:
  - role: included_role

galaxy_info:
  role_name: mysql
  author: me
  description: Example role
  company: "mycompany.org"
  license: "license (BSD, MIT)"
  min_ansible_version: 2.4
  platforms:
    - name: EL
      versions:
        - 6
        - 7
        - 8
    - name: Ubuntu
      versions:
        - all
    - name: Debian
      versions:
        - all
    - name: Archlinux
      versions:
        - all
  galaxy_tags:
    - example
"""

def test_add_role():
    # arrange
    builder = DependencyGraphHelper()
    expected_ouput = """// roles
digraph {
\tnode [color=lightblue2 style=filled]
\tfirst [label=first]
\tsecond [label=second]
}"""

    # act
    builder._add_role("first")
    builder._add_role("second")
    
    content = builder.graph.source
    
    # assert
    assert len(builder._roles) == 2
    assert content == expected_ouput

def test_add_role_doublon():
    # arrange
    builder = DependencyGraphHelper()
    expected_ouput = """// roles
digraph {
\tnode [color=lightblue2 style=filled]
\tfirst [label=first]
\tsecond [label=second]
}"""

    # act
    builder._add_role("first")
    builder._add_role("second")
    builder._add_role("first")
    
    content = builder.graph.source
    
    # assert
    assert len(builder._roles) == 2
    assert content == expected_ouput

def test_add_role_dependency():
    # arrange
    builder = DependencyGraphHelper()
    expected_ouput = """// roles
digraph {
\tnode [color=lightblue2 style=filled]
\tsample_include_role [label=sample_include_role]
\tmain [label=main]
\tmain -> sample_include_role
}"""

    # act
    builder._add_role_dependency("main", "sample_include_role")

    content = builder.graph.source
    
    # assert
    assert len(builder._roles) == 2
    assert content == expected_ouput

def test_search_item():
    # arrange
    file_content = SAMPLE_TASK_FILE
    dependencies_builder = DependencyGraphHelper()
    expected_ouput = """// roles
digraph {
\tnode [color=lightblue2 style=filled]
\tsample_include_role [label=sample_include_role]
\tmain [label=main]
\tmain -> sample_include_role
}"""

    # act
    dependencies_builder._search_item("main", file_content, "include_role")
    print( dependencies_builder.graph._node.title)

    content = dependencies_builder.graph.source
    
    # assert
    assert len(dependencies_builder._roles) == 2
    assert content == expected_ouput
    
def test_search_in_meta():
    # arrange
    file_content = SAMPLE_META_FILE
    dependencies_builder = DependencyGraphHelper()
    expected_ouput = """// roles
digraph {
\tnode [color=lightblue2 style=filled]
\tincluded_role [label=included_role]
\tmain [label=main]
\tmain -> included_role
}"""

    # act
    dependencies_builder._search_in_meta("main", file_content)
    print( dependencies_builder.graph._node.title)

    content = dependencies_builder.graph.source
    
    # assert
    assert len(dependencies_builder._roles) == 2
    assert content == expected_ouput

def test_search_in_metas():
    # arrange
    builder = DependencyGraphHelper()
    expected_graph = Digraph(comment='roles', node_attr={'color': 'lightblue2', 'style': 'filled'})
    expected_graph.node("java",label="java")
    expected_graph.node("elasticsearch", label="elasticsearch")
    expected_graph.edge("elasticsearch", "java")

    # act
    builder._search_in_metas("test-data/roles")

    # assert
    assert len(builder._roles) == 2
    assert builder.graph.source == expected_graph.source

def test_search_in_tasks_for_include_role():
    # arrange
    builder = DependencyGraphHelper()
    expected_graph = Digraph(comment='roles', node_attr={'color': 'lightblue2', 'style': 'filled'})
    expected_graph.node("common",label="common")
    expected_graph.node("net-utils", label="net-utils")
    expected_graph.edge("net-utils", "common")

    # act
    builder._search_in_tasks("test-data/roles", "include_role")

    # assert
    assert len(builder._roles) == 2
    assert builder.graph.source == expected_graph.source