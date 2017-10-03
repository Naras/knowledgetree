package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personHasWorkList")
public class PersonHasWorkList extends EntityQuery<PersonHasWork> {

	private static final String EJBQL = "select personHasWork from PersonHasWork personHasWork";

	private static final String[] RESTRICTIONS = {
			"lower(personHasWork.id.person) like lower(concat(#{personHasWorkList.personHasWork.id.person},'%'))",
			"lower(personHasWork.id.relation) like lower(concat(#{personHasWorkList.personHasWork.id.relation},'%'))",
			"lower(personHasWork.id.work) like lower(concat(#{personHasWorkList.personHasWork.id.work},'%'))",};

	private PersonHasWork personHasWork;

	public PersonHasWorkList() {
		personHasWork = new PersonHasWork();
		personHasWork.setId(new PersonHasWorkId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public PersonHasWork getPersonHasWork() {
		return personHasWork;
	}
}
