
import pytest
from graphviz import Digraph

from ansibledependenciesgraph.main import DependencyGraphHelper


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
