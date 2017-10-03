package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personHasRoleList")
public class PersonHasRoleList extends EntityQuery<PersonHasRole> {

	private static final String EJBQL = "select personHasRole from PersonHasRole personHasRole";

	private static final String[] RESTRICTIONS = {
			"lower(personHasRole.id.person) like lower(concat(#{personHasRoleList.personHasRole.id.person},'%'))",
			"lower(personHasRole.id.role) like lower(concat(#{personHasRoleList.personHasRole.id.role},'%'))",};

	private PersonHasRole personHasRole;

	public PersonHasRoleList() {
		personHasRole = new PersonHasRole();
		personHasRole.setId(new PersonHasRoleId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public PersonHasRole getPersonHasRole() {
		return personHasRole;
	}
}
