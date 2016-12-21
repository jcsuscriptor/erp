from lxml import etree

#Utilizar lxml para manipular XML

root = etree.Element("root")
root.append( etree.Element("child1") )

child2 = etree.SubElement(root, "child2")
child3 = etree.SubElement(root, "child3")

print(etree.tostring(root, pretty_print=True))
