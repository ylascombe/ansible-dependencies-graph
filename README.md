# Ansible Dependencies Graph

[ansible-dependencies-graph](https://github.com/ylascombe/ansible-dependencies-graph) is a python script to create a graph representing your Ansible roles dependencies.

# Prerequisites
 * **Ansible** >= 2.9 code. Even if it is not required by this tool, code parsed should be written on version that contains code with `include_role` and `import_role` and not `include` as before.
 * **pythhon** >= 3.6
 * **graphviz**: The tool used to generate the graph in SVG. 
 ```
 $ sudo apt-get install graphviz # or yum install or brew install
 ```
 
# Install

TODO

# Usage

TODO

# Dev environment

To setup a development environment:
 - Install graphviz `sudo apt-get install graphviz # or yum install or brew install graphviz`
 - pip3 install -r requirements.txt

Run the tests with:
```bash
$ cd tests && pytest dependency-graph-test.py
```

  
## Contribution
Contributions are welcome. Feel free to contribute by creating an issue or submitting a PR :smiley: 
