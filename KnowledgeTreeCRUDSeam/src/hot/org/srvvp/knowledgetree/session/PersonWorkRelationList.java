package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personWorkRelationList")
public class PersonWorkRelationList extends EntityQuery<PersonWorkRelation> {

	private static final String EJBQL = "select personWorkRelation from PersonWorkRelation personWorkRelation";

	private static final String[] RESTRICTIONS = {
			"lower(personWorkRelation.id) like lower(concat(#{personWorkRelationList.personWorkRelation.id},'%'))",
			"lower(personWorkRelation.description) like lower(concat(#{personWorkRelationList.personWorkRelation.description},'%'))",
			"lower(personWorkRelation.name) like lower(concat(#{personWorkRelationList.personWorkRelation.name},'%'))",};

	private PersonWorkRelation personWorkRelation = new PersonWorkRelation();

	public PersonWorkRelationList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public PersonWorkRelation getPersonWorkRelation() {
		return personWorkRelation;
	}
}
