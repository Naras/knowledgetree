package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personPersonRelationList")
public class PersonPersonRelationList extends EntityQuery<PersonPersonRelation> {

	private static final String EJBQL = "select personPersonRelation from PersonPersonRelation personPersonRelation";

	private static final String[] RESTRICTIONS = {
			"lower(personPersonRelation.id) like lower(concat(#{personPersonRelationList.personPersonRelation.id},'%'))",
			"lower(personPersonRelation.description) like lower(concat(#{personPersonRelationList.personPersonRelation.description},'%'))",
			"lower(personPersonRelation.name) like lower(concat(#{personPersonRelationList.personPersonRelation.name},'%'))",};

	private PersonPersonRelation personPersonRelation = new PersonPersonRelation();

	public PersonPersonRelationList() {
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public PersonPersonRelation getPersonPersonRelation() {
		return personPersonRelation;
	}
}
