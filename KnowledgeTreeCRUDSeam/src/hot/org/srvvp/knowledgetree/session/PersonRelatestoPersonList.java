package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityQuery;
import java.util.Arrays;

@Name("personRelatestoPersonList")
public class PersonRelatestoPersonList
		extends
			EntityQuery<PersonRelatestoPerson> {

	private static final String EJBQL = "select personRelatestoPerson from PersonRelatestoPerson personRelatestoPerson";

	private static final String[] RESTRICTIONS = {
			"lower(personRelatestoPerson.id.person1) like lower(concat(#{personRelatestoPersonList.personRelatestoPerson.id.person1},'%'))",
			"lower(personRelatestoPerson.id.person2) like lower(concat(#{personRelatestoPersonList.personRelatestoPerson.id.person2},'%'))",
			"lower(personRelatestoPerson.id.relation) like lower(concat(#{personRelatestoPersonList.personRelatestoPerson.id.relation},'%'))",};

	private PersonRelatestoPerson personRelatestoPerson;

	public PersonRelatestoPersonList() {
		personRelatestoPerson = new PersonRelatestoPerson();
		personRelatestoPerson.setId(new PersonRelatestoPersonId());
		setEjbql(EJBQL);
		setRestrictionExpressionStrings(Arrays.asList(RESTRICTIONS));
		setMaxResults(25);
	}

	public PersonRelatestoPerson getPersonRelatestoPerson() {
		return personRelatestoPerson;
	}
}
