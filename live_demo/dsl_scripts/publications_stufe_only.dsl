LOAD publications;

NODE PublicationLevel
    KEY tree_guid
    NAME resolved_structure_element_name
    FROM publications
    WHERE (children_count > 0);

EDGE Contains
    FROM publications
    SOURCE parent_tree_guid
    TARGET tree_guid
    WHERE (children_count > 0);
