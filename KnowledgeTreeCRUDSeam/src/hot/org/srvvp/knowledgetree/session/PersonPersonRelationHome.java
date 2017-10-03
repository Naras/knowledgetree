package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import java.util.ArrayList;
import java.util.List;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("personPersonRelationHome")
public class PersonPersonRelationHome extends EntityHome<PersonPersonRelation> {

	public void setPersonPersonRelationId(String id) {
		setId(id);
	}

	public String getPersonPersonRelationId() {
		return (String) getId();
	}

	@Override
	protected PersonPersonRelation createInstance() {
		PersonPersonRelation personPersonRelation = new PersonPersonRelation();
		return personPersonRelation;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
	}

	public boolean isWired() {
		return true;
	}

	public PersonPersonRelation getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

	public List<PersonRelatestoPerson> getPersonRelatestoPersons() {
		return getInstance() == null
				? null
				: new ArrayList<PersonRelatestoPerson>(getInstance()
						.getPersonRelatestoPersons());
	}

}
